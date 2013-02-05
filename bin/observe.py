#!/usr/bin/python

class Observation:
    """
    object to accumulate signal observations into a sample
    """
    def __init__(self, sig_str,isAP=False, avgsize=10, bytes=0):
        self.ss_sum = sig_str
        self.ss_sum_squares = sig_str^2
        self.AP = isAP
        self.bytes_sum = bytes
        self.count=1
        self.avgsize=avgsize    # no of obs for rolling average
        self.rolling_samples = []

    def add(self, sig_str, bytes=0):
        self.ss_sum += sig_str
        self.ss_sum_squares += sig_str^2
        self.bytes_sum += bytes
        self.count+=1
        #for rolling average keep last avgsize samples 
        if len(rolling_samples) < self.avgsize:
            rolling_samples.append(sig_str)
        else:
            rolling_samples.pop(0)
            rolling_samples.append(sig_str)

    def avg_sig(self):
        return   self.ss_sum / self.count
    
    #std variance of sample = E[x^2] - (E[x])^2
    def var_sig(self):
        return (self.ss_sum_squares/self.count - self.avg_sig()^2)

    
    def rolling_avg(self):
        return sum(rolling_avg)/len(rolling_avg)

    def rolling_var(self):
        sumsquares = sum([ x^2 : x in self.rollingsamples])
        return sumsquares/len(rolling_avg) - self.rolling_avg()^2

       

