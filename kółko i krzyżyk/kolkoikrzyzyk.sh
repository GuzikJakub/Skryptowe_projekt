#!/bin/bash

tablica=(0 1 2 3 4 5 6 7 8 9)
gameover=0
while [ "$gameover" == 0 ]
do
			echo -n "Podaj pozycje dla X (od 0 do 8): "
			read zmienna
			tablica[$zmienna]="X"
			for x in {0..2}
			do
				echo -n ${tablica[x]} 
				echo -n " | "
			done
			echo ""
			for x in {3..5}
			do
				echo -n ${tablica[x]}
				echo -n " | "
			done
			echo ""
			for x in {6..8}
			do
				echo -n ${tablica[x]}
				echo -n " | "
			done
			echo ""

			if [ "${tablica[0]}${tablica[1]}${tablica[2]}" == "XXX" ] || [ "${tablica[3]}${tablica[4]}${tablica[5]}" == "XXX" ] || [ "${tablica[6]}${tablica[7]}${tablica[8]}" == "XXX" ] || [ "${tablica[0]}${tablica[3]}${tablica[6]}" == "XXX" ] || [ "${tablica[1]}${tablica[4]}${tablica[7]}" == "XXX" ] || [ "${tablica[3]}${tablica[5]}${tablica[9]}" == "XXX" ];
			then
				echo "wygrał gracz 1"
				gameover=1

			else 
			echo -n "Podaj pozycje dla O (od 0 do 8): "
			read zmienna
			tablica[$zmienna]="O"
			for x in {0..2}
			do
				echo -n ${tablica[x]} 
				echo -n " | "
			done
			echo ""
			for x in {3..5}
			do
				echo -n ${tablica[x]}
				echo -n " | "
			done
			echo ""
			for x in {6..8}
			do
				echo -n ${tablica[x]}
				echo -n " | "
			done
			echo ""
			if [ "${tablica[0]}${tablica[1]}${tablica[2]}" == "OOO" ] || [ "${tablica[3]}${tablica[4]}${tablica[5]}" == "OOO" ] || [ "${tablica[6]}${tablica[7]}${tablica[8]}" == "OOO" ] || [ "${tablica[0]}${tablica[3]}${tablica[6]}" == "OOO" ] || [ "${tablica[1]}${tablica[4]}${tablica[7]}" == "OOO" ] || [ "${tablica[3]}${tablica[5]}${tablica[9]}" == "OOO" ];
			then
				echo "wygral gracz 2"
				gameover=1
			fi
			fi

done
