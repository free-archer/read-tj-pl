use warnings FATAL => 'all';
use strict;
use utf8;
use Data::Dumper::Simple;
use Perl6::Say;

binmode(STDIN,':utf8');
binmode(STDOUT,':utf8');

my $start = localtime();

my $filename = '21103114.log';
open(my $fh, '<:encoding(UTF-8)', $filename)
    or die "Could not open file '$filename' $!";

my @arr;
my $str_log = "";
my @arrtj;

while (my $str = <$fh>) {
    chomp $str;

    if ($str =~ /([0-9]{2}):([0-9]{2})\.([0-9]+)\-([0-9]+)\,(\w+)\,(\d+)/) {
        if (length($str_log)) {
            push(@arr, $str_log);
        }
        $str_log = $str;
    }
    else {
        $str_log = join("-#-", $str_log, $str);
    }
}
say scalar @arr;

for (my $i=0; $i<scalar @arr; $i++) {
    my %tj;
    while ($arr[$i] =~ m/,([A-Za-z0-9_А-Яа-я:]+)=([^,]+)/g) {
        $tj{$1} = $2;
    }
    push(@arrtj, \%tj);
}
say scalar @arrtj;
#warn Dumper @arrtj;

say localtime();
my $duration = localtime() - $start;
say ($duration);
