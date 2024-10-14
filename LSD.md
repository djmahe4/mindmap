
Half Adder and Full Adder are digital circuits used for binary addition.

*Half Adder:*

1. Adds two binary digits (bits)
2. Produces sum and carry outputs
3. No carry input

*Full Adder:*

1. Adds three binary digits (bits)
2. Produces sum and carry outputs
3. Has carry input

Key differences:
```

| Feature            | Half Adder                                | Full Adder                                |
| :----------------- | :--------------------------------------- | :--------------------------------------- |
| Inputs             | 2 (A, B)                                  | 3 (A, B, Cin)                             |
| Outputs            | 2 (Sum, Carry)                            | 2 (Sum, Carry)                            |
| Carry Input        | No                                        | Yes (Cin)                                  |
| Carry Output       | Yes                                       | Yes                                       |
| Number of Gates    | 2 (XOR, AND)                              | 4 (2 XOR, 2 AND, 1 OR)                    |
| Application        | Simple arithmetic operations              | Complex arithmetic operations, ALUs       |

*Half Adder Truth Table:*

| A   | B   | Sum | Carry |
| :-- | :-- | :-- | :---- |
| 0   | 0   | 0   | 0     |
| 0   | 1   | 1   | 0     |
| 1   | 0   | 1   | 0     |
| 1   | 1   | 0   | 1     |

*Full Adder Truth Table:*

| A   | B   | Cin | Sum  | Carry |
| :-- | :-- | :-- | :--- | :---- |
| 0   | 0   | 0   | 0    | 0     |
| 0   | 0   | 1   | 1    | 0     |
| 0   | 1   | 0   | 1    | 0     |
| 0   | 1   | 1   | 0    | 1     |
| 1   | 0   | 0   | 1    | 0     |
| 1   | 0   | 1   | 0    | 1     |
| 1   | 1   | 0   | 0    | 1     |
| 1   | 1   | 1   | 1    | 1     |
```
*Implementation:*

Half Adder:

```
vhdl
entity half_adder is
    Port ( A : in  STD_LOGIC;
           B : in  STD_LOGIC;
           Sum : out  STD_LOGIC;
           Carry : out  STD_LOGIC);
end half_adder;

architecture Behavioral of half_adder is
begin
    Sum <= A xor B;
    Carry <= A and B;
end Behavioral;
```

Full Adder:

```
vhdl
entity full_adder is
    Port ( A : in  STD_LOGIC;
           B : in  STD_LOGIC;
           Cin : in  STD_LOGIC;
           Sum : out  STD_LOGIC;
           Carry : out  STD_LOGIC);
end full_adder;

architecture Behavioral of full_adder is
begin
    Sum <= A xor B xor Cin;
    Carry <= (A and B) or (A and Cin) or (B and Cin);
end Behavioral;
```
