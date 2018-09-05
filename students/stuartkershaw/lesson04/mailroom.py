#!/usr/bin/env python3

import json_save.json_save.json_save_meta as js

import pathlib
pth = pathlib.Path('./')


class Donor:

    def __init__(self, name):
        self._name = name
        self._donations = []
        self._rollup = {}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if not val:
            raise ValueError("A Donor must have a name.")
        self._name = val

    @property
    def donations(self):
        return self._donations

    def add_donation(self, val):
        if val < 1:
            raise ValueError("A positive donation value is required.")
        self.donations.append(val)

    @property
    def rollup(self):
        return self._rollup

    @rollup.setter
    def rollup(self, val):
        if not val:
            raise ValueError("Rollup values are required.")
        self._rollup = val


class DonorList:

    def __init__(self):
        self._donors = {}

    @property
    def donors(self):
        return self._donors

    @donors.setter
    def donors(self, donorListLoaded):
        if not donorListLoaded:
            raise ValueError("Donors data is required.")
        self._donors = {}
        for name, donations in donorListLoaded.items():
            self.add_donor(name)
            for d in donations:
                self.donors[name].add_donation(d)

    def add_donor(self, name):
        donor = Donor(name)
        self.donors[donor.name] = donor

    def get_donor(self, name):
        if not name:
            raise ValueError("Please provide a donor name.")

        if name in self.donors:
            return self.donors[name]
        else:
            return "Donor not found."

    def get_donations(self, name):
        if not name:
            raise ValueError("Please provide a donor name.")

        if name in self.donors:
            return self.donors[name].donations
        else:
            return "Donor not found."

    def compose_thank_you(self, donor):
        if not donor:
            raise ValueError("Please provide a donor.")

        message_obj = {
            'donor_name': donor.name,
            'donations': sum(donor.donations)
        }
        message = 'Dear {donor_name}, thanks so much '\
                  'for your generous donations in the amount of: '\
                  '${donations}.'.format(**message_obj)
        return message

    def get_donor_names(self):
        print("\n".join([donor for donor in self.donors]))

    def generate_rollup(self):
        for donor in self.donors:
            cur_donor = self.donors[donor]
            number = len(cur_donor.donations)
            total = sum(cur_donor.donations)
            average = float(
                format(
                    sum(cur_donor.donations) / len(cur_donor.donations), '.2f')
                )
            cur_donor.rollup = dict(zip(('number', 'total', 'average'),
                                        (number, total, average)))

    def generate_table(self):
        if not self.donors:
            print('The list of donors is empty.')
            return
        self.generate_rollup()
        headings = ('Donor Name', 'Num Gifts', 'Total Given', 'Average Gift')
        print('{:20}{:<15}{:<15}{:<15}'.format(*headings))
        print('{:_<65}'.format(''))
        for donor in self.donors:
            cur_donor = self.donors[donor]
            print('{:<20}'.format(cur_donor.name),
                                 ('{:<15}' * len(cur_donor.rollup))
                  .format(*cur_donor.rollup.values()))

    def generate_letters(self):
        if not self.donors:
            print('The list of donors is empty.')
            return
        self.generate_rollup()
        for donor in self.donors:
            with open(donor.replace(' ', '_') + '.txt', 'w') as outfile:
                outfile.write(self.compose_thank_you(self.donors[donor]))
        print('Letters generated: ')
        for f in pth.iterdir():
            if '.txt' in str(f):
                print(f)


class DonorCli:

    def __init__(self, donorCollection):
        self._donorCollection = donorCollection

    @property
    def donorCollection(self):
        return self._donorCollection

    def set_donor(self):
        while True:
            try:
                name = input('Please enter a donor name: ')
                if not name:
                    raise ValueError
            except ValueError:
                print('Oops, name is required.')
                return
            else:
                self.donorCollection.add_donor(name)
                self.set_donation(name)
                print('{} added. Current donors: '.format(name))
                self.donorCollection.get_donor_names()
                return

    def set_donation(self, donor):
        while True:
            try:
                donation = int(input('Please enter a donation amount: '))
                if not donation > 0:
                    raise ValueError
            except ValueError:
                print('Please provide a whole number greater than zero.')
            else:
                self.donorCollection.donors[donor].add_donation(donation)
                print('${} donation received.'.format(donation))
                self.get_selection()

    def accept_donation(self):
        if not self.donorCollection.donors:
            print('The list of donors is empty.')
            return
        instruction = 'Please enter a full name '\
                      'or type \'list\' to see donors:\n'
        name_input = input(instruction)
        if name_input == 'list':
            self.donorCollection.get_donor_names()
            self.accept_donation()
        elif name_input in self.donorCollection.donors:
            self.set_donation(name_input)
        else:
            print('Donor not found.')

    def save_donations(self):
        donorsToJson = {}
        for donor in self.donorCollection.donors:
            cur_donor = self.donorCollection.donors[donor]
            donorsToJson[cur_donor.name] = cur_donor.donations
        donorsSaved = DonorPersist(donorsToJson)
        try:
            with open('donorList.json', 'w') as outfile:
                donorsSaved.to_json(outfile)
                print('Successfully saved donors to JSON file.')
        except IOError as e:
            print('Couldn\'t save donors to JSON file. {}'.format(e))

    def load_donations(self):
        try:
            with open('donorList.json') as infile:
                reconstructed = js.from_json(infile)
                self.donorCollection.donors = reconstructed.donors
                print('Successfully loaded donors from JSON file.')
        except IOError as e:
            print('Couldn\'t load donors from JSON file. {}'.format(e))

    def apply_selection(self, selection):
        arg_dict = {
            '1': self.set_donor,
            '2': self.accept_donation,
            '3': self.donorCollection.generate_table,
            '4': self.donorCollection.generate_letters,
            '5': self.save_donations,
            '6': self.load_donations,
            '7': quit
        }
        try:
            if not arg_dict.get(selection):
                raise KeyError
            arg_dict.get(selection)()
        except KeyError:
            print('Oops, invalid selection.')

    def get_selection(self):
        options = 'Please select from the menu:\n'\
                  '1) add new donor\n'\
                  '2) log donation\n'\
                  '3) create a report\n'\
                  '4) send letters to everyone\n'\
                  '5) save donations data\n'\
                  '6) load donations data\n'\
                  '7) quit\n'
        while True:
            selection = input(options)
            self.apply_selection(selection)
            if selection == '2':
                self.get_selection()


class DonorPersist(js.JsonSaveable):

    donors = js.Dict()

    def __init__(self, donors):
        self.donors = donors


def main():
    dl = DonorList()
    cli = DonorCli(dl)
    cli.get_selection()


if __name__ == "__main__":
    main()
