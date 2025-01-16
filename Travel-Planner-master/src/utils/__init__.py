def to_fixed(num, digits):
	# Convert number to have fixed number of digits else pad with zeros
	return str(num).rjust(digits, '0')

def time_format(hour, minutes):
	# Convert hour and minute to string representation 00:00
	return f'{ to_fixed(hour, 2) }:{ to_fixed(minutes, 2) }'