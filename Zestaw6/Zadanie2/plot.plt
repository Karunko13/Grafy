set term pdf size 8, 8
set key autotitle columnhead


set grid
set output "before.pdf"
plot "before.dat" using 1:2 with linespoint \
pt 7 ps 1 lc 2
set output "after.pdf"
plot "after.dat" using 1:2 with linespoint \
pt 7 ps 1 lc 2