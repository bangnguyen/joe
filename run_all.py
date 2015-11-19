from subprocess import call
from joe.utils.allfunctions import *


def string_to_second(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)


if __name__ == "__main__":
    now = time.strftime("%H:%M:%S %d/%m/%Y")
    start = time.time()
    for i in range(1, 9):
        call("scrapy crawl f%s" % (i), shell=True)
    end = time.time()
    duration = end - start
    es_client.index(index=index_name, doc_type="reports",
                    body={"start at": now, "duration": string_to_second(duration)})

