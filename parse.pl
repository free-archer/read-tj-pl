use warnings FATAL => 'all';
use strict;
use utf8;
use Data::Dumper::Simple;
use Perl6::Say;
use DateTime qw( );
use DBI;

binmode(STDIN,':utf8');
binmode(STDOUT,':utf8');

#SQL CONNECT
my $dsn = 'DBI:ODBC:Driver={SQL Server}';
my $db_server = "localhost";
my $db_name = "tempdb";
my $db_user = "sa";
my $db_pass = "cnhtkjr";
my $db_table = "tj";
##

my $filename = '21103114.log';
#my $filename = 'test.log';
open(my $fh, '<:encoding(UTF-8)', $filename)
    or die "Could not open file '$filename' $!";

#"([0-9]{2}):([0-9]{2})\.([0-9]+)\-([0-9]+)\,(\w+)\,(\d+)"
#",([A-Za-z0-9_А-Яа-я:]+)=([^,]+)"

my @arr;
my @temp;
my $str_log = "";
my @properties;
my @main;

my @columns = qw(id time event level);

#PARSE FILE
while (my $str = <$fh>) {
    chomp $str;

    if ($str =~ /([0-9]{2}:[0-9]{2}\.[0-9]+\-[0-9]+)\,(\w+)\,(\d+)/)
    {


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
for (my $i=0; $i<scalar @arr; $i++) {
    my $str = $arr[$i];

    my ($y,$m,$d,$h) = $filename =~ /^([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})/ or die;
    my ($mm,$ss) = $str =~ /([0-9]{2}):([0-9]{2})\./ or die;
    my ($id,$event,$level) = $str =~ /([0-9]{2}:[0-9]{2}\.[0-9]+\-[0-9]+)\,(\w+)\,(\d+)/ or die;
    my $datetime = DateTime->new(
        year      => "20".$y,
        month     => $m,
        day       => $d,
        hour       => $h,
        minute     => $mm,
        second     => $ss,
        time_zone => 'local',
    );

    my %tj = (
        "time"=>$datetime->datetime(),
        "id"=>$id,
        "event"=>$event,
        "level"=>$level,
    );

    while ($arr[$i] =~ m/,([A-Za-z0-9_А-Яа-я:]+)=([^,]+)/g) {
        unless (grep(/^$1$/, @columns)) {
            push(@columns, $1);
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

say scalar @columns;
my @quote_columns = map {qq|"$_"|} @columns;
#warn Dumper $properties[0];

#SQL
my $dbh = DBI->connect("$dsn;Server=$db_server;Database=$db_name", $db_user, $db_pass) or die "Database connection not made: $DBI::errstr";
warn Dumper $dbh;
#$db_table = "tbl1";
my $sth_create = $dbh->prepare("SELECT * FROM SYSOBJECTS WHERE NAME='$db_table' ");
say "sth_create";
warn Dumper $sth_create;

if (0) {
    #CREATE TABLE
    #my @quote_columns = map{$dbh->quote($_)} @columns;
    #warn Dumper @quote_columns;

    my $sql_create_table = "CREATE TABLE $db_table (";
    foreach my $column (@quote_columns) {
        $sql_create_table = $sql_create_table . $column . " varchar(255), ";
    }
    $sql_create_table = $sql_create_table . ");";

    say $sql_create_table;

    my $sth_create_table = $dbh->prepare($sql_create_table);
    $sth_create_table->execute()  or die "TABLE was not created: $DBI::errstr";
}

#INSERT DATA INTO TABLE
#my $sql_insert = "INSERT INTO $db_table (" . join(", ", @quote_columns) . " VALUES (" . join(", ", @properties[@_]) . ");";
my $col = "";
my $val = "";

# my $tt = $properties[1];
 #warn Dumper $properties[0];
#print $properties[0];
# say $tt->{"p:processName"};
foreach my $prop (@properties) {
    $col = "";
    $val = "";
    my $len = scalar @columns;
    for (my $i = 0; $i < $len; $i++) {
        my $column = $columns[$i];
        $col = $col . "$quote_columns[$i], ";
        if (exists $prop->{$column}) {
            $val = $val . "\"$prop->{$column}\", ";
        }
    }
}
$col =~ s/, *$//;
$val =~ s/, *$//;
# warn Dumper $col;
# warn Dumper $val;
my $sql_insert = "INSERT INTO $db_table ($col) VALUES($val);";

say $sql_insert;
my $sth = $dbh->prepare($sql_insert);
my $res = $sth->execute();
say $res;


$dbh->disconnect();