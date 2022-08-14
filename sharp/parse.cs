using System.Diagnostics;
using System.Text.RegularExpressions;

internal class Parse {
    private static void Main(String[] args) {
      Stopwatch stopwatch = new Stopwatch();
      stopwatch.Start();

      //VARS
      List<String> mainArray= new List<String>();
      String filename = "../21103114.log";

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
            mainArray.Add(str);
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

    stopwatch.Stop();
    Console.WriteLine($"Done! Run time: {stopwatch.ElapsedMilliseconds}");
    }
}