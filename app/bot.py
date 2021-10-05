########################################################################################################
#    Class that automates a user's strategy, keeping track of balances, profits and placing orders.    #
########################################################################################################

class Bot:
    def __init__(self, strategyName, config, saveData=None) -> None:
        self.config = config
        if saveData is not None:
            self.__load_from_save(saveData)
        else:
            self.__first_time_setup()

        self.load_strategy(strategyName)

    def __generic_setup(self, data) -> None:
        self.balance = data['balance']
        self.accountValue = data['value']
        self.dryRun = data['dryRun']

    def __first_time_setup(self) -> None:
        self.balance = self.config['startingBalance']
        self.accountValue = self.balance
        self.dryRun = self.config['dryRun']

    def __load_from_save(self) -> None:
        pass

    def load_strategy(self, name) -> None:
        pass

    def tick(self):
        pass

    def __save_progress(self):
        pass

    def __update_balances_and_pnl(self):
        pass