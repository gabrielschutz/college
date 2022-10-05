library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ula is

	port(
		A, B											:	in		unsigned   		  (3 downto 0);
		PB1, PB2										:	in		std_logic;
		R									 			:	out 	unsigned   		  (4 downto 0);
		DSSa, DSSb, DSSc, DSSd, DSSe, DSSf	:	out	std_logic_vector (6 downto 0)
	);
	
end entity ula;

architecture main of ula is

begin

	process (PB1)
	
		variable Atemp			: unsigned (4 downto 0);
		variable Btemp			: unsigned (4 downto 0);
		variable Temp4b		: unsigned (3 downto 0);
		variable Temp5b		: unsigned (4 downto 0);
		variable Op				: integer := 0;
		
		begin
			
			Temp5b := "00000";
		
			Atemp(4) := '0';
			Atemp(3 downto 0) := A;
			
			Btemp(4) := '0';
			Btemp(3 downto 0) := B;
			
			if (rising_edge(PB1)) then
				Op := Op + 1;
			end if;
				
			if (Op >= 6) then
				Op := 0;
			end if;
			
			if (Op = 0) then
				Temp5b := Atemp + Btemp;
				
			elsif (Op = 1) then
				if (Atemp >= Btemp) then
					Temp5b := Atemp - Btemp;
				else
					Temp5b := Btemp - Atemp;
					Temp5b(4) := '1';
				end if;
				
			elsif (Op = 2) then
				Temp5b(4) := '0';
				Temp4b := A and B;
				Temp5b(3 downto 0) := Temp4b;
				
			elsif (Op = 3) then
				Temp5b(4) := '0';
				Temp4b := A or B;
				Temp5b(3 downto 0) := Temp4b;
				
			elsif (Op = 4) then
				Temp5b(4) := '0';
				Temp4b := A xor B;
				Temp5b(3 downto 0) := Temp4b;
				
			elsif (Op = 5) then
				Temp5b(4) := '0';
				Temp4b := not A;
				Temp5b(3 downto 0) := Temp4b;
				
			end if;
			
			case Op is
					
				when 0 => 
					DSSf <= "1000000"; --'0'
					DSSe <= "0001000"; --'A'
				when 1 => 
					DSSf <= "1111001"; --'1'
					DSSe <= "0010010"; --'S'
				when 2 =>
					DSSf <= "0100100"; --'2'
					DSSe <= "0001000"; --'A'
				when 3 =>
					DSSf <= "0110000"; --'3'
					DSSe <= "1000000"; --'O'
				when 4 =>
					DSSf <= "0011001"; --'4'
					DSSe <= "0001001"; --'X'
				when 5 =>
					DSSf <= "0010010"; --'5'
					DSSe <= "1000110"; --'C'
				when others => DSSf <= "0000110"; --'E'
					
			end case;
			
			if (PB2 = '0') then
			
				R <= Temp5b;
				
				DSSe <= "1111111";
				DSSd <= "1111111";
				DSSc <= "1111111";
				
				if (Op = 0) then
				
					case Temp5b is
                    
						  when "00000" => 
                        DSSb <= "1000000"; --0
                        DSSa <= "1000000"; --0
                    
						  when "00001" =>
                        DSSb <= "1000000"; --0
                        DSSa <= "1111001"; --1
                    
						  when "00010" =>
                        DSSb <= "1000000"; --0
                        DSSa <= "0100100"; --2
                    when "00011" =>
                        DSSb <= "1000000"; --0
                        DSSa <= "0110000"; --3
                    when "00100" =>
                        DSSb <= "1000000"; --0    
                        DSSa <= "0011001"; --4
                    when "00101" =>
                        DSSb <= "1000000"; --0
                        DSSa <= "0010010"; --5									
                    when "00110" =>
                        DSSb <= "1000000"; --0    
                        DSSa <= "0000010"; --6
                    when "00111" =>
                        DSSb <= "1000000"; --0                
                        DSSa <= "1111000"; --7
                    when "01000" =>
                        DSSb <= "1000000"; --0    
                        DSSa <= "0000000"; --8
                    when "01001" =>
                        DSSb <= "1000000"; --0    
                        DSSa <= "0011000"; --9
                    when "01010" => --10
                        DSSb <= "1111001"; --1    
                        DSSa <= "1000000"; --0
                    when "01011" => --11
                        DSSb <= "1111001"; --1  
                        DSSa <= "1111001"; --1
                    when "01100" => --12
                        DSSb <= "1111001"; --1    
                        DSSa <= "0100100"; --2
                    when "01101" => --13
                        DSSb <= "1111001"; --1    
                        DSSa <= "0110000"; --3
                    when "01110" => --14
                        DSSb <= "1111001"; --1    
                        DSSa <= "0011001"; --4
                    when "01111" => --15
                        DSSb <= "1111001"; --1    
                        DSSa <= "0010010"; --5
                    when "10000" => --16
                        DSSb <= "1111001"; --1
                        DSSa <= "0000010"; --6
                    when "10001" => --17
                        DSSb <= "1111001"; --1    
                        DSSa <= "1111000"; --7
                    when "10010" => --18
                        DSSb <= "1111001"; --1    
                        DSSa <= "0000000"; --8
                    when "10011" => --19
                        DSSb <= "1111001"; --1    
                        DSSa <= "0011000"; --9
                    when "10100" => --20
                        DSSb <= "0100100"; --2    
                        DSSa <= "1000000"; --0
                    when "10101" => --21
                        DSSb <= "0100100"; --2    
                        DSSa <= "1111001"; --1
                    when "10110" => --22
                        DSSb <= "0100100"; --2    
                        DSSa <= "0100100"; --2
                    when "10111" => --23
                        DSSb <= "0100100"; --2    
                        DSSa <= "0110000"; --3
                    when "11000" => --24
                        DSSb <= "0100100"; --2    
                        DSSa <= "0011001"; --4
                    when "11001" => --25
                        DSSb <= "0100100"; --2    
                        DSSa <= "0010010"; --5
                    when "11010" => --26
                        DSSb <= "0100100"; --2    
                        DSSa <= "0000010"; --6
                    when "11011" => --27
                        DSSb <= "0100100"; --2    
                        DSSa <= "1111000"; --7
                    when "11100" => --28
                        DSSb <= "0100100"; --2    
                        DSSa <= "0000000"; --8
                    when "11101" => --29
                        DSSb <= "0100100"; --2    
                        DSSa <= "0011000"; --9
                    when "11110" => --30
                        DSSb <= "0110000"; --3    
                        DSSa <= "1000000"; --0        
                    when others =>
                        DSSb <= "1111111";-- desligado
                        DSSa <= "0000110";
                end case;
					 
				elsif (Op = 1) then
					
					if (Temp5b(4) = '1') then
						DSSc <= "0111111";
					end if;
					
					case Temp5b(3 downto 0) is
                    
						when "0000" => 
							DSSb <= "1000000"; --0
							DSSa <= "1000000"; --0
					  
						when "0001" =>
							DSSb <= "1000000"; --0
							DSSa <= "1111001"; --1
					  
						when "0010" =>
							DSSb <= "1000000"; --0
							DSSa <= "0100100"; --2
						when "0011" =>
							DSSb <= "1000000"; --0
							DSSa <= "0110000"; --3
						when "0100" =>
							DSSb <= "1000000"; --0    
							DSSa <= "0011001"; --4
						when "0101" =>
							DSSb <= "1000000"; --0
							DSSa <= "0010010"; --5									
						when "0110" =>
							DSSb <= "1000000"; --0    
							DSSa <= "0000010"; --6
						when "0111" =>
							DSSb <= "1000000"; --0                
							DSSa <= "1111000"; --7
						when "1000" =>
							DSSb <= "1000000"; --0    
							DSSa <= "0000000"; --8
						when "1001" =>
							DSSb <= "1000000"; --0    
							DSSa <= "0011000"; --9
						when "1010" => --10
							DSSb <= "1111001"; --1    
							DSSa <= "1000000"; --0
						when "1011" => --11
							DSSb <= "1111001"; --1  
							DSSa <= "1111001"; --1
						when "1100" => --12
							DSSb <= "1111001"; --1    
							DSSa <= "0100100"; --2
						when "1101" => --13
							DSSb <= "1111001"; --1    
							DSSa <= "0110000"; --3
						when "1110" => --14
							DSSb <= "1111001"; --1    
							DSSa <= "0011001"; --4
						when "1111" => --15
							DSSb <= "1111001"; --1    
							DSSa <= "0010010"; --5
				
					end case;
					
				else
				
					case Temp5b(0) is
					
						when '0' => DSSa <= "1000000"; --'0'
						when '1' => DSSa <= "1111001"; --'1'
						
					end case;
					
					case Temp5b(1) is
					
						when '0' => DSSb <= "1000000"; --'0'
						when '1' => DSSb <= "1111001"; --'1'
						
					end case;
					
					case Temp5b(2) is
					
						when '0' => DSSc <= "1000000"; --'0'
						when '1' => DSSc <= "1111001"; --'1'
						
					end case;
					
					case Temp5b(3) is
					
						when '0' => DSSd <= "1000000"; --'0'
						when '1' => DSSd <= "1111001"; --'1'
						
					end case;
					
					case Temp5b(4) is
					
						when '0' => DSSe <= "1000000"; --'0'
						when '1' => DSSe <= "1111001"; --'1'
						
					end case;
					
				end if;
	
			end if;
				
	end process;
		
end architecture main;
