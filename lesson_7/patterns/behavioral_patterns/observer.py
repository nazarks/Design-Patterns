# поведенческий паттерн - наблюдатель
# Курс
class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):
    def update(self, subject):
        for i in range(len(subject.students) - 1):
            print((f"SMS->{subject.students[i]}", "к нам присоединился", subject.students[-1].name))


class EmailNotifier(Observer):
    def update(self, subject):
        for i in range(len(subject.students) - 1):
            print((f"EMAIL->{subject.students[i]}", "к нам присоединился", subject.students[-1].name))
