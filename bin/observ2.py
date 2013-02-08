#!/usr/bin/python

class Observation:
    """
    object to accumulate signal observations into a sample
    """
    def __init__(self, sig_str, bytes=0,subtype='',time=0,freq='',ssid='',wifitype='' ):
        self.count=1
        self.avgsize=30    # no of obs for rolling average
        self.rolling_samples = []
        self.bytes=bytes
        self.subtype=subtype
        self.time=time
        self.freq=freq
        self.ssid=ssid
        self.wifitype=wifitype
        self.localcount=0

    def ssid():
        return self.ssid

    def is_number(str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def getlocalcount(self):
        """
        everytime value is read reset to zero. incr by add (signal sample)
        """
        result = self.localcount
        self.localcount=0
        return result

    def add(self, sig_str, bytes=0,subtype='',time=0,freq='',ssid='',wifitype='' ):
    #def add(self, sig_str, bytes, subtype, time, freq, ssid, wifitype):
        if len(sig_str)>0:
            self.count+=1
            self.localcount+=1
            if (len(subtype)>0):
                self.subtype=subtype
            self.time=time
            self.freq=freq
            if(len(ssid)>0):
                self.ssid=ssid
            self.wifitype=wifitype
            #for rolling average keep last avgsize samples 
            if len(self.rolling_samples) < self.avgsize:
                self.rolling_samples.append(int(sig_str))
            else:
                self.rolling_samples.pop(0)
                self.rolling_samples.append(int(sig_str))


    def rolling_avg(self):
        size=len(self.rolling_samples)
        if size>0:   
            return sum(self.rolling_samples)/size
        else:
            return 0

    #def rolling_var(self):
    #    sumsquares = sum([ x^2 for x in self.rolling_samples])
    #    denom =  len(self.rolling_samples) - self.rolling_avg()^2
    #    if (denom == 0):
    #        return 0
    #    else:
    #        return sumsquares/denom
    def rolling_var(self):
      if (len(self.rolling_samples) == 0):
        return 0
      xbar=float(self.rolling_avg())
      var = ([ (x - xbar) for x in self.rolling_samples])
      var = [ x*x for x in var] 
      var = sum(var)/float(len(self.rolling_samples))
      return var 
