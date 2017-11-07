%define the colors
color(red).
color(green). 
color(blue).


%define connected(stateA, stateB) which expresses that two states are 
%successfully connected if they have both different colors

not_same(red, green).
not_same(red, blue).

not_same(green, red).
not_same(green,  blue).

not_same(blue, red).
not_same(blue, green).



connected(StateA, StateB):- not_same(StateA, StateB).
neighbors(StateA, StateB):- connected(StateA, StateB); connected(StateB,StateA).

india(M,C,O,T,G,KA,AP,KE,TN):-neighbors(M,C),neighbors(M,T),neighbors(M,G),neighbors(M,KA), neighbors(C,O), 
neighbors(C,T), neighbors(O,T), neighbors(O,AP), neighbors(T,KA), neighbors(T,AP), neighbors(G,KA),
neighbors(KA,AP), neighbors(KA,KE), neighbors(KA,TN), neighbors(AP,TN), neighbors(KE,TN).

