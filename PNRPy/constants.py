
from enum import Enum

URL="http://railenquiry.in/enquiry/api/pnr.php?pnr=%s&security=high"

class Status(Enum):
	CONFIRMED = 1
	WAITING = 2
	INVALID_PNR=3