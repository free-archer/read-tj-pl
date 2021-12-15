use warnings FATAL => 'all';
use strict;
use utf8;
use Data::Dumper::Simple;
use Perl6::Say;
use Cwd;
use Time::Seconds;
use Time::Piece;

use Win32::Console;
use Win32::Unicode::File;

binmode(STDIN,':utf8');
binmode(STDOUT,':utf8');

Win32::Console::OutputCP( 65001 );


my $start = Time::Seconds->new(localtime);

my $cwd = getcwd();
my $filename = "$cwd/test/read.txt";
open(my $fh, '<:encoding(UTF-8)', $filename)
    or die "Could not open file '$filename' $!";


while (my $str = <$fh>) {
    chomp $str;
    print "$str\n";

}
my $stop = Time::Seconds->new(localtime);

say $start;
say $stop;