import functions
import xy
import settings


def main():
    serv = functions.server()
    #functions.system(serv=serv)
    #functions.disk_usage(serv=serv)
    functions.get_wifi_clients(serv=serv)
if __name__=='__main__':
    main()


#xy.send_report(serv, settings.ALIENWARE, settings.SCRAPER, settings.WARNING, msg='Testing the newly configured xymon client.' )