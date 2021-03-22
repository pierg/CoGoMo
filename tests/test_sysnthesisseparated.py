






if __name__ == '__main__':

    ie = "sa1"
    se = "(G((sa1 & ra1) -> X sa1) & G((sa1 & ra2) -> ((X sa2) | (X sa1))) & G((sa1 & rz) -> ((X sz) | (X sa1))) & G((sa2 & ra2) -> X sa2) & G((sa2 & ra1) -> ((X sa1) | (X sa2))) & G((sa2 & rz) -> ((X sz) | (X sa2))) & G((sb1 & rb1) -> X sb1) & G((sb1 & rb2) -> ((X sb2) | (X sb1))) & G((sb1 & rz) -> ((X sz) | (X sb1))) & G((sb2 & rb2) -> X sb2) & G((sb2 & rb1) -> ((X sb1) | (X sb2))) & G((sb2 & rz) -> ((X sz) | (X sb2))) & G((sz & rz) -> X sz) & G((sz & ra1) -> ((X sa1) | (X sz))) & G((sz & ra2) -> ((X sa2) | (X sz))) & G((sz & rb1) -> ((X sb1) | (X sz))) & G((sz & rb2) -> ((X sb2) | (X sz))) & G(((sa1 & ! sa2 & ! sb1 & ! sb2 & ! sz) | (sa2 & ! sa1 & ! sb1 & ! sb2 & ! sz) | (sb1 & ! sa1 & ! sa2 & ! sb2 & ! sz) | (sb2 & ! sa1 & ! sa2 & ! sb1 & ! sz) | (sz & ! sa1 & ! sa2 & ! sb1 & ! sb2))))"
    le = "(G(F (ra1 -> X sa1)) & G(F (ra2 -> X sa2)) & G(F (rb1 -> X sb1)) & G(F (rb2 -> X sb2)) & G(F (rz -> X sz)))"

    iss = "(true)"
    ss = "(G(((ra1 & ! ra2 & ! rb1 & ! rb2 & ! rz) | (ra2 & ! ra1 & ! rb1 & ! rb2 & ! rz) | (rb1 & ! ra1 & ! ra2 & ! rb2 & ! rz) | (rb2 & ! ra1 & ! ra2 & ! rb1 & ! rz) | (rz & ! ra1 & ! ra2 & ! rb1 & ! rb2))) & G(sa1 -> X(ra1 | ra2 | rz)) & G(sa2 -> X(ra2 | ra1 | rz)) & G(sb1 -> X(rb1 | rb2 | rz)) & G(sb2 -> X(rb2 | rb1 | rz)) & G(sz -> X(rz | ra1 | ra2 | rb1 | rb2)))"
    ls = "(F sb2)"

    sep = f"({ie} -> {iss}) & ({ie} -> "


