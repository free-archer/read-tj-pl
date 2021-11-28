use warnings FATAL => 'all';
use strict;
use utf8;
use Data::Dumper::Simple;
use Perl6::Say

binmode(STDIN,':utf8');
binmode(STDOUT,':utf8');

my $filename = '21103114.log';
#my $filename = 'test.log';
open(my $fh, '<:encoding(UTF-8)', $filename)
    or die "Could not open file '$filename' $!";

#"([0-9]{2}):([0-9]{2})\.([0-9]+)\-([0-9]+)\,(\w+)\,(\d+)"
#",([A-Za-z0-9_А-Яа-я:]+)=([^,]+)"

my @arr;
my @temp;
my $str_log = "";
#my %tj;
my @properties;
my @main;

my @column = qw(time event level);

#PARSE FILE
while (my $str = <$fh>) {
    chomp $str;

    #($str =~ /([0-9]{2}):([0-9]{2})\.([0-9]+)\-([0-9]+)\,(\w+)\,(\d+)/)
    if ($str =~ /([0-9]{2}:[0-9]{2}\.[0-9]+\-[0-9]+)\,(\w+)\,(\d+)/)
    {
        say $&;
        my %main = (
            "time"=>$1,
            "event"=>$2,
            "level"=>$3,
        );
        push(@main, \%main);

        # warn Dumper(@main);
        # say scalar @main;

        if (length($str_log)) {
            push(@arr, $str_log);
            #say $str_log;
        }
        $str_log = $str;
    }
    else    {
        $str_log = join("-#-", $str_log, $str);
        #say $str_log;
    }
}

say scalar @arr;

#GET PROPERTIES
#foreach my $n (@arr) {
for (my $i=0; $i<scalar @arr; $i++) {
    #say $i . " - " . $arr[$i];
    #say;

    my %tj;
    while ($arr[$i] =~ m/,([A-Za-z0-9_А-Яа-я:]+)=([^,]+)/g) {
        unless (grep(/^$1$/, @column)) {
            push(@column, $1);
        }

        if ($1 eq "Sql") {
            $tj{$1} = split(/=#=/, $2);
        }
        else {
            $tj{$1} = $2;
        }
    }
    push(@properties, \%tj);
}

say scalar @column;
warn Dumper $properties[0];
