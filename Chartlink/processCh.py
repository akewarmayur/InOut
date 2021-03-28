from common.gAPI import GoogleAPI
from common.sheetOperations import SheetOps
import threading
from scrapCh import ScrapData

class ProcessCh:

    def __init__(self):
        self.objGAPI = GoogleAPI()
        self.objSheet = SheetOps()
        self.SheetName = 'CIEconfig'
        self.objScrap = ScrapData()

    def download_config_files(self, service):
        # Download all supporting files in helpers foler if doesn't exists
        self.objGAPI.download_files(service, 'yolo/stock.cfg', "1O6ass4NlCZEE7nR_xtnfmuTCz8vpdbIq")
        # file_id = search_file(service, 'obj.names', 'text/plain', "folder_id")
        self.objGAPI.download_files(service, 'yolo/obj.names', '1S1WrjCejTBREO4jpoWRuEcD5U524001u')
        self.objGAPI.download_files(service, 'yolo/stock_4000.weights', '1Ybpt9vdTxrlS7n56MIR7qlS71GU8NMio')

    def readConfigStatus(self):
        try:
            content = self.objSheet.readSheet(self.SheetName, 'ChartConfig')
            value = [row[1] for row in content if row[0] == 'EndlessLoop']
            status = value[0].lower()
        except Exception as exReadSheet:
            print(exReadSheet)

    def readMachineNameStocks(self, machine_name):
        try:
            content = self.objSheet.readSheet(self.SheetName, 'ChartStocks', machine_name)
            content = content['SID']
            return content
        except Exception as exReadSheet:
            print(exReadSheet)

    def readNoOfThread(self):
        try:
            content = self.objSheet.readSheet(self.SheetName, 'ChartConfig')
            value = [row[1] for row in content if row[0] == 'num_worker_threads']
            return value[0]
        except Exception as exReadSheet:
            print(exReadSheet)

    def start(self, machine_name):
        service = self.objGAPI.intiate_gdAPI()
        self.download_config_files(service)

        status = self.readConfigStatus()
        print(status)

        if status == 'TRUE':
            while True:
                print("yes=====================")
                status = self.readConfigStatus()
                threads = []
                if status == 'TRUE':
                    arr = self.readMachineNameStocks(machine_name)
                    num_worker_threads = int(self.readNoOfThread())
                    print("num_worker_threads===", num_worker_threads)
                    start = 0
                    end = 10
                    for i in range(num_worker_threads):
                        value = arr[start:end]
                        start = end
                        end = end + 10
                        t = threading.Thread(target=self.objScrap.scrap, args=(value,))
                        t.start()
                        threads.append(t)

                    # join all threads
                    for t in threads:
                        t.join()

                else:
                    arr = self.readMachineNameStocks(machine_name)
                    num_worker_threads = int(self.readNoOfThread())
                    print("num_worker_threads===", num_worker_threads)
                    start = 0
                    end = 10
                    # threads = []
                    for i in range(num_worker_threads):
                        value = arr[start:end]
                        start = end
                        end = end + 10
                        t = threading.Thread(target=self.objScrap.scrap, args=(value,))
                        t.start()
                        threads.append(t)

                    # join all threads
                    for t in threads:
                        t.join()
                    break

        else:
            print("first else================")
            arr = self.readMachineNameStocks()
            num_worker_threads = int(self.readNoOfThread())
            print("num_worker_threads===", num_worker_threads)
            start = 0
            end = 10
            threads = []
            for i in range(num_worker_threads):
                value = arr[start:end]
                print(start, end)
                start = end
                end = end + 10
                t = threading.Thread(target=self.objScrap.scrap, args=(value,))
                t.start()
                threads.append(t)

            # join all threads
            for t in threads:
                t.join()



obj = ProcessCh()
obj.start()
