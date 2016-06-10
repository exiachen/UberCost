import requests
import sys
from pyquery import PyQuery as pq
import setting
import re
import cairo
import pycha.line

reload(sys)
sys.setdefaultencoding('utf-8')

url_pattern = "https://riders.uber.com.cn/trips?page=%d"
costs = {}
pattern = re.compile(r'\d+')

CANCEL_STRING = u'\u5df2\u53d6\u6d88'

def Parser(reply):
	doc = pq(reply)
	trips = doc(".trip-expand__origin")
	if len(trips) == 0:
		return False

	for trip in trips:
		childtd = []
		for c in trip.iterchildren():
			childtd.append(c)

		date = pattern.findall(childtd[1].text_content())
		year = date[0]
		month = date[1]
		day = date[2]
		print "year: %s, month: %s, day: %s" % (year, month, day)

		cost = childtd[3].text_content().strip(u'\xa0')
		if cost == CANCEL_STRING or cost == '':
			continue
		else:
			cost = float(cost[1:])
		print "cost: ", cost

		if year in costs:
			if month in costs[year]:
				if day in costs[year][month]:
					costs[year][month][day].append(cost)
				else:
					costs[year][month][day] = [cost]
			else:
				costs[year][month] = {day: [cost]}
		else:
			costs[year] = {month: {day: [cost]}}


	return True

def Spider():
	url_index = 1

	while True:
		url = url_pattern % url_index
		url_index += 1

		r = requests.get(url, headers = setting.HEADERS)
		if not Parser(r.text):
			break


def Analysis():
	cost_per_year = {}
	cost_per_month = {}
	for year in costs.keys():
		count = 0
		total_cost = 0
		for month in costs[year].keys():
			total_cost_per_month = 0
			for day in costs[year][month].keys():
				count += len(costs[year][month][day])
				total_cost_per_month += sum(costs[year][month][day])

			total_cost += total_cost_per_month
			if year in cost_per_month:
				cost_per_month[year].append((int(month), total_cost_per_month))
			else:
				cost_per_month[year] = [(int(month), total_cost_per_month)]

		cost_per_month[year].sort()
		cost_per_year[year] = {"count": count, "total_cost": total_cost}

	#print cost_per_month

	for key in cost_per_year.keys():
		print "year: %s" % key
		print "\tuser uber: %d times, cost: %.02f" % (cost_per_year[key]["count"], cost_per_year[key]["total_cost"])

	data_set = ((key, tuple(cost_per_month[key])) for key in cost_per_month.keys())
	return tuple(data_set)

def Drawline(data_set):
	surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,600,600)
	options = {
		'legend':{'hide':False}, 
		'title':'uber cost(by exiachen)', 
		'titleColor':'#0000ff', 
		'background':{'chartColor': '#ffffff'}, 
		'axis':{'labelColor':'#ff0000'},
		}

	chart = pycha.line.LineChart(surface,options)
	chart.addDataset(data_set)
	chart.render()
	surface.write_to_png('result.png')



if __name__ == '__main__':
	Spider()
	data_set = Analysis()
	Drawline(data_set)
