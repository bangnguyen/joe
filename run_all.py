from subprocess import call



if __name__ == "__main__":
    call("scrapy crawl f1", shell=True)
    call("scrapy crawl f2", shell=True)
