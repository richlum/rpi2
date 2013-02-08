#!/usr/bin/python

class Observation:
    """
    object to accumulate signal observations into a sample
    """
    def __init__(self, sig_str,isAP=False, avgsize=30, bytes=0):
        self.count=1
        self.avgsize=avgsize    # no of obs for rolling average
        self.rolling_samples = []
        bytes=0;
        subtype=''
        time=0
        freq=''
        ssid=''
        wifitype=''

    def is_number(str):
        try:
            int(str)
            return True
        except ValueError:
            return False


    def add(self, sig_str, bytes, subtype, time, freq, ssid, wifitype):
        if len(sig_str)>0:
            self.count+=1
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

    def rolling_var(self):
        sumsquares = sum([ x^2 for x in self.rolling_samples])
        denom =  len(self.rolling_samples) - self.rolling_avg()^2
        if (denom == 0):
            return 0
        else:
            return sumsquares/denom
