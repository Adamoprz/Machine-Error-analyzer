from App import *
from Window import *

Directory =  os.getcwd()
SRC = Directory + '\\data\\'
OUT = Directory + '\\data_new\\'

#folders = ["d" + str(i) for i in range(1,  13, 1)]
#folders = ["d13_test", "d14_test"]
#folders = ["d4"]
folders = [" "]
def main():

    app = App(SRC, OUT)
    app.init()
    app.df_to_csv(Directory + "csv.csv")

    wind = QApplication(sys.argv)
    window = ChartWindow(app.get_dataframe())
    window.show()
    sys.exit(wind.exec())


if __name__ == "__main__":
    main()