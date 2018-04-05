from sortedcontainers import SortedList
from structs import Segment, Pixel, SweepLine as SL, Point
from common import hot, current, line, segments

def segment_endpoint_answer(point, segment):
	pixel = Pixel(point)
	if pixel not in current:
		# до этого в пикселе не было обнаружено критических точек
		heat_answer(pixel)
	# если событие -- начало отрезка
	if point == segment.start:
		pixel.segs.append(segment)
		# игнорируем ту часть отрезка, что лежит внутри пикселя
		intersection = segment.intersects(pixel)
		if intersection is not None:
			line.push(SL.Event(SL.Event.Type.SEG_REINSERT, intersection, segment=segment, pixel=pixel))
	# если событие -- конец отрезка
	else:
		line.remove(segment)

def segseg_intersection_answer(point):
	pixel = Pixel(point)
	if pixel not in current:
		heat_answer(pixel)

def segpix_intersection_answer(point, segment, pixel):
	# добавляем отрезок в соответствующий список
	if pixel.is_on_top(point):
		pixel.upper.add(segment)
	else:
		pixel.lower.add(segment)
	pixel.segs.append(segment)
	# игнорируем фрагмент отрезка, находящийся внутри пикселя
	line.remove(segment)
	# TODO FIXME INTERSECTS TO THE RIGHT OF POINT
	intersection = segment.intersects(pixel)
	if intersection is not None and intersection.x > point.x:
		line.push(SL.Event(SL.Event.Type.SEG_REINSERT, intersection, segment=segment, pixel=pixel))

def segment_reinsertion_answer(point, segment, pixel):
	line.insert(segment)
	if pixel.is_on_top(point):
		pixel.upper.add(segment)
	elif pixel.is_on_bottom(point):
		pixel.lower.add(segment)

	neighbour = pixel.get_neighbour(point)
	if neighbour in current:
		segpix_intersection_answer(point, neighbour, segment)

def pixel_end_answer(point, pixel):
	if pixel.is_on_top(point):
		line.remove(pixel.top())
	else:
		line.remove(pixel.bottom())
	hot.extend(current)
	current.clear()

def heat_answer(pixel):
	current.add(pixel)
	l = []
	for s in segments:
		intersection = s.intersects(pixel)
		if (intersection is not None and intersection.x < line.xpos):
			l.append(s)

	for segment in l:
		pixel.segs.append(segment)
		intersection = segment.intersects(pixel)
		if intersection is not None:
			line.remove(segment)
			line.push(SL.Event(SL.Event.Type.SEG_REINSERT, intersection, segment=segment, pixel=pixel))
	# pix.build()
	top, bottom = pixel.top(), pixel.bottom()
	line.insert(top)
	line.push(SL.Event(SL.Event.Type.PIX_END, top.end, pixel=pixel))
	line.insert(bottom)
	line.push(SL.Event(SL.Event.Type.PIX_END, bottom.end, pixel=pixel))
