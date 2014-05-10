# -*- coding: utf-8 -*- 
class YakuTripleCalc:
    _dice = []
    _value = 0
     
    def __init__(self, dice, value):
        self._dice = dice
        self._value = value

    def yaku_point(self):
        rdice = self.select_value_mach_and_rollable()
        if(len(rdice) >= 3):
            self.dice_set_disrollable(rdice, 3)
            return self._value * 100
        else:
            return 0
        
    def select_value_mach_and_rollable(self):
        rdice = []
        for die in self._dice:
            if(self._value == die.value and die.is_rollable):
                rdice.append(die)
        return rdice

    def dice_set_disrollable(self, dice, counter):
        i = 0
        while(i < counter):
            dice[i].is_rollable = False
            i += 1

class YakuTriple1Calc(YakuTripleCalc):
    
    def __init__(self, dice, value):
        super().__init__(dice, value)

    def yaku_point(self):
        if(self._value != 1):
            return 0

        rdice = self.select_value_mach_and_rollable()
        if(len(rdice) >= 3):
            self.dice_set_disrollable(rdice, 3)
            return 1000
        else:
            return 0

class YakuSingleCalc:
    _dice=[]
    _value=0
    
    def __init__(self, dice, value):
        self._dice = dice
        self._value = value
    
    def yaku_point(self):
        point = 0;
        rdice = []
        
        for die in self._dice:
            if(self._value == die.value and die.is_rollable):
                rdice.append(die);
                if(self._value == 1):
                    point += 100
                else:
                    point += self._value * 10

        for die in rdice:
            die.is_rollable = False
        
        return point

class PointCalc:
    dice = []
    _counter=0 
    
    def __init__(self):
        pass
    
    def roll_dice(self):
        self._counter = 0
        for die in self.dice:
            if(die.is_rollable):
                self._counter += 1
                die.roll_die()
           
    def get_roll_point(self):
        point = 0
        i = 0
        
        while(i < self._counter / 3):
            point += YakuTriple1Calc(self.dice, 1).yaku_point()
            point += YakuTripleCalc(self.dice, 2).yaku_point()
            point += YakuTripleCalc(self.dice, 3).yaku_point()
            point += YakuTripleCalc(self.dice, 4).yaku_point()
            point += YakuTripleCalc(self.dice, 5).yaku_point()
            point += YakuTripleCalc(self.dice, 6).yaku_point()
            i += 1
                
        point += YakuSingleCalc(self.dice, 1).yaku_point()
        point += YakuSingleCalc(self.dice, 5).yaku_point()
        
        return point