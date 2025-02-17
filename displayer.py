from commons import WORK_TYPE


class Displayer:

    def print(self, data):

        tasks = data["tasks"]
        print("=========\n\n")
        print("----Tasks----:\n")
        for work_type in WORK_TYPE:
            print(f"=> {work_type}: ")
            for task in filter(lambda t: t.state() == work_type, tasks):
                print(task)
        print("\n=========\n")
