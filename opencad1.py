# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 12:00:00 2019

@author: prateekspawar
"""

import openpyscad as ops
l=10;b=20;h=40
c1 = ops.Cube([l, h, b]).translate([-l/2,-h/2,-b/2]).translate([10,10,-10])

(c1).write("sample.scad")