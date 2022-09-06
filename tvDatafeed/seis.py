import tvDatafeed

class Seis(object): # TODO: add a __repr__ method so user can easily see what Seis contains
    """
    Symbol, exchange and interval data set
    
    Holds a unique set of symbol, exchange and interval 
    values in addition to keeping a set of consumers 
    instances for this set.
    
    Parameters
    ----------
    symbol : str 
        ticker string for symbol
    exchange : str
        exchange where symbol is listed
    interval : tvDatafeed.Interval
        chart interval
    
    Methods
    -------
    new_consumer(callback)
        Create a new consumer and add to Seis
    del_consumer(consumer)
        Remove consumer from Seis
    get_hist(n_bars)
        Get historic data for this Seis
    del_seis()
        Remove Seis from tvDatafeedLive where it is
        listed
    get_consumers()
        Return a list of consumers for this Seis
    """

    def __init__(self, symbol, exchange, interval):
        self._symbol=symbol
        self._exchange=exchange
        self._interval=interval
        
        self._tvdatafeed=None 
        self._consumers=[]
        self.updated=None # datetime of the data bar that was last retrieved from TradingView
    
    def __eq__(self, other):
        # Compare two seis instances to decide if they are equal
        #
        # Instances are equal if symbol, exchange and interval attributes
        # are of same value.
        if isinstance(other, self.__class__): # make sure that they are the same class 
            if self.symbol == other.symbol and self.exchange == other.exchange and self.interval == other.interval: # these attributes need to be identical
                return True
        # TODO : add an option to compare Seis with list and tuple containing 3 string elements (symb, exch, inter)
        
        return False
    
    def __repr__(self):
        return f'Seis("{self._symbol}","{self._exchange}",{self._interval})'
    
    def __str__(self):
        return "symbol='"+self._symbol+"',exchange='"+self._exchange+"',interval='"+self._interval.name+"'"

    @property # read-only attribute
    def symbol(self):
        return self._symbol
    
    @property # read-only attribute
    def exchange(self):
        return self._exchange
    
    @property # read-only attribute
    def interval(self):
        return self._interval
    
    @property
    def tvdatafeed(self):
        return self._tvdatafeed
    
    @tvdatafeed.setter
    def tvdatafeed(self, value):
        if (self._tvdatafeed) is not None:
            raise AttributeError("Cannot overwrite attribute, need to delete it first")
        elif not isinstance(value, tvDatafeed.TvDatafeedLive):
            raise ValueError("Argument must be instance of TvDatafeed") 
        else:
            self._tvdatafeed=value
    
    @tvdatafeed.deleter
    def tvdatafeed(self):
        self._tvdatafeed=None
    
    def new_consumer(self, callback):
        '''
        Create a new consumer and add to Seis
        
        Parameters
        ----------
        callback : func
            function to call when new data produced
        
        Returns
        -------
        tvdatafeed.Consumer
        
        Raises
        ------
        NameError
            if no TvDatafeedLive reference is added for this Seis
        '''
        if self._tvdatafeed is None:
            raise NameError("TvDatafeed not provided")
        
        return self._tvdatafeed.new_consumer(self, callback) # methods go through tvdatafeed to acquire lock and make it thread safe
    
    def del_consumer(self, consumer):
        '''
        Remove consumer from Seis
        
        Parameters
        ----------
        consumer : tvdatafeed.Consumer
            consumer instance
        
        Raises
        ------
        NameError
            if no TvDatafeedLive reference is added for this Seis
        '''
        if self._tvdatafeed is None:
            raise NameError("TvDatafeed not provided")
        
        self._tvdatafeed.del_consumer(consumer) 
    
    def add_consumer(self, consumer):
        # Add consumer into Seis, not for direct use
        #
        # This methods is not for direct calling by the
        # user, but for TvDatafeedLive instance to 
        # perform operations in the background.
        #
        # Parameters
        # ----------
        # consumer : tvdatafeed.Consumer
        #     consumer instance
        self._consumers.append(consumer)
        
    def pop_consumer(self, consumer):
        # Remove consumer from Seis, not for direct use
        #
        # This methods is not for direct calling by the
        # user, but for TvDatafeedLive instance to 
        # perform operations in the background.
        #
        # Parameters
        # ----------
        # consumer : tvdatafeed.Consumer
        #    consumer instance
        if consumer not in self._consumers:
            raise NameError("Consumer does not exist in the list")
        self._consumers.remove(consumer)
        
    def get_hist(self, n_bars): # TODO: implement this method
        '''
        Get historic data for this Seis
        
        This method is not implemented!
        
        Parameters
        ----------
        n_bars : int
            number of historic bars to retrieve
        '''
        raise NotImplementedError 
    
    def del_seis(self):
        '''
        Remove Seis from tvDatafeedLive where it is
        listed
        '''
        if self._tvdatafeed is None:
            raise NameError("TvDatafeed not provided")
        
        self._tvdatafeed.del_seis(self)
    
    def get_consumers(self):
        '''
        Return a list of consumers for this Seis
        
        Returns
        -------
        list
            contains all consumer instances registered 
            for this Seis
        '''
        return self._consumers
    