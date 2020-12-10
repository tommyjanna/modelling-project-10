CONJECTUREPANEL Conjectures
PROOF "P, (¬Q→P)→(P→S) ⊢ S"
INFER P,
     (¬Q→P)→(P→S)
     ⊢ S 
FORMULAE
0 S,
1 P,
2 P→S,
3 ¬Q→P,
4 (¬Q→P)→P→S,
5 ¬Q,
6 (¬Q→P)→(P→S)
IS
SEQ (cut[B,C\3,0]) ("→ intro"[A,B\5,1]) (hyp[A\1]) (cut[B,C\2,0]) ("→ elim"[A,B\3,2]) (hyp[A\4]) (hyp[A\3]) (cut[B,C\0,0]) ("→ elim"[A,B\1,0]) (hyp[A\2]) (hyp[A\1]) (hyp[A\0])
END
CONJECTUREPANEL Conjectures
PROOF "(A∧¬P)→Q, ¬Q ⊢ ¬(A∧¬P)"
INFER (A∧¬P)→Q,
     ¬Q 
     ⊢ ¬(A∧¬P)
FORMULAE
0 ¬(A∧¬P),
1 ¬Q,
2 A∧¬P→Q,
3 A∧¬P,
4 Q,
5 ¬(A∧¬P),
6 (A∧¬P)→Q 
IS
SEQ (cut[B,C\5,0]) ("→ MT"[A,B\3,4]) (hyp[A\2]) (hyp[A\1]) (hyp[A\0])
END
CONJECTUREPANEL Conjectures
PROOF "(A∧P)∨(B∧P) ⊢ P→(A∨B)"
INFER (A∧P)∨(B∧P)
     ⊢ P→(A∨B)
FORMULAE
0 A∨B,
1 B,
2 A,
3 B∧P,
4 P,
5 A∧P,
6 A∧P∨B∧P,
7 (A∧P)∨(B∧P)
IS
SEQ ("→ intro"[A,B\4,0]) ("∨ elim"[A,B,C\5,3,0]) (hyp[A\6]) (cut[B,C\2,0]) (LAYOUT "∧ elim" (0) ("∧ elim(L)"[A,B\2,4]) (hyp[A\5])) (cut[B,C\0,0]) (LAYOUT "∨ intro" (0) ("∨ intro(L)"[B,A\1,2]) (hyp[A\2])) (hyp[A\0]) (cut[B,C\1,0]) (LAYOUT "∧ elim" (0) ("∧ elim(L)"[A,B\1,4]) (hyp[A\3])) (cut[B,C\0,0]) (LAYOUT "∨ intro" (0) ("∨ intro(R)"[B,A\2,1]) (hyp[A\1])) (hyp[A\0])
END
