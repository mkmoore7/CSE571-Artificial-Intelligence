%define the colors
color(red).
color(green). 
color(blue).
color(yellow).

%define the states
state(M).
state(C).
state(O).
state(T).
state(G).
state(KA).
state(AP).
state(KE).
state(TN).

%define connected(stateA, stateB) which expresses that two states are 
%successfully connected if they have both different colors

not_same(red, green).
not_same(red, blue).
not_same(red, yellow).
not_same(green, red).
not_same(green,  blue).
not_same(green, yellow).
not_same(blue, red).
not_same(blue, green).
not_same(blue, yellow).
not_same(yellow, red).
not_same(yellow, green).
not_same(yellow, blue).

connected(StateA, StateB):- not_same(StateA, StateB).


/*
%neighborship
neighborship(StateA, StateB):- not_same()



india(M,C,O,T,G,KA,AP,KE,TN):- 
*/