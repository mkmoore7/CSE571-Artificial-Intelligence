
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% Fact Base %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% First we introduce the fact of a position. A position can be a number
pos(1).
pos(2).
pos(3).
pos(4).
pos(5).
pos(6).

/*

Input: ?- pos(3)
Output: true.

Input: ?- pos(11)
Output: false.

*/

% Here we state which number is equal to which (a number is only equal to itself)
equal(1,1).
equal(2,2).
equal(3,3).
equal(4,4).
equal(5,5).
equal(6,6).
equal(7,7).
equal(8,8).

/*

Input: ?- equal(5,5).
Output: true.

Input: ?- equal(5,4).
Output: false.

Input: ?- equal(4,X).
Output: X=4.

*/

% A function defining the successor of a number
% For example, 2 is the successor of 1
succ(1,2).
succ(2,3).
succ(3,4).
succ(4,5).
succ(5,6).

/*

Input: ?- succ(3,X).
Output: X=4.

Input: ?- succ(X,4).
Output: X=3.

*/


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% Basic Rules %%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% A coordinate consists of two positional values
coord(X,Y) :- pos(X),pos(Y).

%%%%%%%%%%%%%%%%%
% The diagonal rule is true if two coordinates are on the same diagonal
% We will state two rulse, since we have two diagonals: one to the left and one to the right : \ and /

% This is a recursiv function, meaning that we need a base/anchor to stop the recursion
% The basic case is, when the two coordinates are equal
diagonal(X1,Y1,X2,Y2) :- equal(X1,X2),equal(Y1,Y2).

% Case: /
% Increase the X1 and Y1 coordinate by one and check if they are diagonal (recursive call)
% This will become true if both coordinates are on a diagonal and (X1,Y1) is lower than (X2,Y2)
diagonal(X1,Y1,X2,Y2) :- succ(X1,A), succ(Y1,B), diagonal(A,B,X2,Y2).
% This will become true if both coordinates are on a diagonal and (X2,Y2) is lower than (X1,Y1)
diagonal(X1,Y1,X2,Y2) :- succ(X2,A), succ(Y2,B), diagonal(X1,Y1,A,B).

% Case: \
% Recursive Anchor
diagonal2(X1,Y1,X2,Y2) :- equal(X1,X2),equal(Y1,Y2).
% Decrease X1 and increase Y1 by one and check if they are diagonal (recursive call)
% This will become true if both coordinates are on a diagonal and (X1,Y1) is lower than (X2,Y2)
diagonal2(X1,Y1,X2,Y2) :- succ(A,X1), succ(Y1,B), diagonal2(A,B,X2,Y2).
% Decrease X2 and increase Y2 by one and check if they are diagonal (recursive call)
% This will become true if both coordinates are on a diagonal and (X2,Y2) is lower than (X1,Y1)
diagonal2(X1,Y1,X2,Y2) :- succ(A,X2), succ(Y2,B), diagonal2(X1,Y1,A,B).
%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% Problem Specific Rules %%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Two coordinates are not diagonal to each other iff not diagonal and not diagonal2 holds (Cases \ and /)
nondiagonal(X1,Y1,X2,Y2) :- \+diagonal(X1,Y1, X2, Y2), \+diagonal2(X1,Y1, X2, Y2).

% Two coordinates are not in the same cross on the field iff they have not the same x coordinate and y coordinate (Case - and |, vertical and horizontal)
noncross(X1,Y1,X2,Y2) :- \+equal(X1,X2), \+equal(Y1,Y2).

%We name two coordinates conflict free if they are not diagonal, vertical or horizontal to each other
conflictfree(X1, Y1, X2, Y2) :- coord(X1,Y1),coord(X2,Y2), nondiagonal(X1,Y1,X2,Y2), noncross(X1,Y1,X2,Y2).





%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Question %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Now we have to formulate our Question which we would like to ask Prolog
% We assume we have six dames and want to solve the 6-Dame-Problem

%This is the not so smart way to solve this
%We first place dame 1 and then all the other dames (2-6) such that they do not conflict with dame 1
%In the next line we check if dame 2 is not in conflict to dames 3-6 (which is likely since we placed them alread)
% If there is a conflict we have to backtrack to resolve the conflict
% This evaluation will take a veeeeeery long time...
eightdame(X1,Y1,X2,Y2,X3,Y3,X4,Y4,X5,Y5,X6,Y6) :- 
conflictfree(X1,Y1,X2,Y2), conflictfree(X1,Y1,X3,Y3), conflictfree(X1,Y1,X4,Y4), conflictfree(X1,Y1,X5,Y5), conflictfree(X1,Y1,X6,Y6),
conflictfree(X2,Y2,X3,Y3), conflictfree(X2,Y2,X4,Y4), conflictfree(X2,Y2,X5,Y5), conflictfree(X2,Y2,X6,Y6), 
conflictfree(X3,Y3,X4,Y4), conflictfree(X3,Y3,X5,Y5), conflictfree(X3,Y3,X6,Y6), 
conflictfree(X4,Y4,X5,Y5), conflictfree(X4,Y4,X6,Y6), 
conflictfree(X5,Y5,X6,Y6).


%This is the smart way to do it
% First we place dame 1 and 2 such that they are not in conflict to each other
% Then we place dame 3 such that dame 3 is not in conflict to dame 1 and 2
% If there is a conflict and we have to backtrack, we just have to move one dame per backtrack and
% we ensure that always all placed dames are not in conflict to each other
% This is also how you as a human would solve the problem :)

eightdameSmart(X1,Y1,X2,Y2,X3,Y3,X4,Y4,X5,Y5,X6,Y6) :-
conflictfree(X2,Y2,X1,Y1),
conflictfree(X3,Y3,X2,Y2), conflictfree(X3,Y3,X1,Y1),
conflictfree(X4,Y4,X1,Y1), conflictfree(X4,Y4,X2,Y2), conflictfree(X4,Y4,X3,Y3),
conflictfree(X5,Y5,X1,Y1), conflictfree(X5,Y5,X2,Y2), conflictfree(X5,Y5,X3,Y3), conflictfree(X5,Y5,X4,Y4),
conflictfree(X6,Y6,X1,Y1), conflictfree(X6,Y6,X2,Y2), conflictfree(X6,Y6,X3,Y3), conflictfree(X6,Y6,X4,Y4), conflictfree(X6,Y6,X5,Y5).
