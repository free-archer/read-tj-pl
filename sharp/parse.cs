using System.Diagnostics;
using System.Text.RegularExpressions;

internal class Parse {
    private static void append_to_dict(Dictionary<String, String>  D_params, MatchCollection matchesp) {
      foreach (Match matchp in matchesp) {
        GroupCollection groupsp = matchp.Groups;
        String value = groupsp[2].Value;
        value = value.Replace("'","").Replace("''","").Replace("-#-", @"\n");

        D_params.Add(groupsp[1].Value.ToLower(), value);
      }

    }

    private static void Main(String[] args) {
      Stopwatch stopwatch = new Stopwatch();
      stopwatch.Start();

      //VARS
      List<String> mainArray= new List<String>();
      Dictionary<String, String> Dict_params;
      List<Dictionary<String, String>> lparams = new List<Dictionary<String, String>>();

      String filename = "21103114.log";

      if (!File.Exists(filename)) {
        Console.WriteLine($"File {filename} do not exist!");
        System.Environment.Exit(1);
      }
        
      //READ TJ
      //1. Создаем массив строк склеивая их по регулярному выражению
      String str_log = "";
      string[] Lines = File.ReadAllLines(filename);
      foreach (string str in Lines) {
        str.Trim();

        Regex rx = new Regex(@"\d{2}:\d{2}.\d{6}-\d");
        if (rx.IsMatch(str)) {
          if (str_log != "") {
            mainArray.Add(str_log);
          }

          str_log = str;
        } else {
          str_log = str_log+"-#-"+str;
        }
        //Console.WriteLine(str_log);
      }

      Console.WriteLine($"Длинна массива: {mainArray.Count}");
      Console.WriteLine($"Время чтения файла: {stopwatch.ElapsedMilliseconds}");

      //2. Получаем список параметров
      Regex rxf = new Regex(@"(\d{2})(\d{2})(\d{2})(\d{2})");
      MatchCollection matches = rxf.Matches(filename);
      Match match = matches[0];
      GroupCollection groups = match.Groups;

      String year = "20"+groups[1].Value;
      String month = groups[2].Value;
      String day = groups[3].Value;
      String hour = groups[4].Value;

      foreach (String arelem in mainArray) {
        String elem = arelem;
        Regex rxt = new Regex(@"(\d{2}):(\d{2}).(\d{6})");
        MatchCollection matchest = rxt.Matches(elem);
        Match matcht = matchest[0];
        GroupCollection groupst = matcht.Groups;

        String minute = groupst[1].Value;
        String second = groupst[2].Value;
        String msec = groupst[3].Value;

        String date_time_str = $"{year}-{month}-{day} {hour}:{minute}:{second}.{msec}";

        Dict_params = new Dictionary<string, string>();
        Dict_params.Add("time", date_time_str);

        String[] re_patterns = new String[3] {@",(\w+)='([^']+)", ",(\\w+)=\"([^\"]+)", @",([A-Za-z0-9А-Яа-я:]+)=([^,]+)"};
        foreach (String pattern in re_patterns) {
          Regex rxp = new Regex(pattern);
          MatchCollection matchesp = rxp.Matches(elem);
          if (matchesp.Count > 0) {
            append_to_dict(Dict_params, matchesp);

            elem = Regex.Replace(elem, pattern, "");
          }

        }

        if (Dict_params.Count > 0 ) {
          lparams.Add(Dict_params);
        }

      }
      


    stopwatch.Stop();
    Console.WriteLine($"Done! Run time: {stopwatch.ElapsedMilliseconds}");
    }
}