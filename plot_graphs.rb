#!/usr/bin/ruby
require 'uri'
require 'net/http'
require 'json'
require 'time'
require 'gnuplot' 

def make_plot(dates, values, title, measure, range=nil)
  Gnuplot.open do |gp|
    Gnuplot::Plot.new( gp ) do |plot|
    
      plot.xdata :time
      plot.format 'x "%m/%Y'
      plot.timefmt '"%Y-%m-%d\\n%H:%M"'
      plot.xtics '25920000'
      plot.xtics 'font ", 6"'
      plot.xrange "['#{dates[0]}':'#{dates[-1]}']"
      plot.yrange range if range != nil
      plot.title  title
      plot.xlabel "Year"
      plot.ylabel measure

      
      plot.data << Gnuplot::DataSet.new( [dates,values] ) do |ds|
        ds.with = "lines"
        ds.linewidth = 2
        ds.using = '1:2'
      end
      
    end
  end
end

def plot_file_complexity(dates, values)
  make_plot(dates,values, "File Complexity Evolution", "File Complexity", "[0:50]")
end

def plot_overall_size(dates, values)
  make_plot(dates,values, "Size Evolution", "Lines")
end
project = 'hadoop'
uri = URI.parse("http://inferno.stilingue.com.br:9780/api/timemachine/index")
req = Net::HTTP::Get.new(uri.to_s)
req.set_form_data ( {
    "resource" => project,
    "metrics" => "file_complexity,lines",
})
res_complexity = Net::HTTP.start(uri.host, uri.port) {|http|
    http.request(req)
  } 

# puts res.body
data = JSON.parse res_complexity.body
metrics = data[0]["cols"][0]["metric"]
dates = Array.new
complexity_values = Array.new
number_of_lines = Array.new
data[0]["cells"].each do |cell| 
  dates << Time.strptime(cell['d'],"%Y-%m-%dT%H:%M:%S%z").iso8601.to_s #.utc.strftime("%Y-%m-%d %H:%M:%S")
  complexity_values  << "%.2f" % cell['v'][0]
  number_of_lines << "%.2f" % cell['v'][1]
end

plot_file_complexity(dates,complexity_values)
plot_overall_size(dates,number_of_lines)
#puts dates
# puts values

# Gnuplot.open do |gp|
#   Gnuplot::Plot.new( gp ) do |plot|
#   
#     plot.xdata :time
#     plot.format 'x "%m/%Y'
#     plot.timefmt '"%Y-%m-%d\\n%H:%M"'
#     plot.xtics '25920000'
#     plot.xtics 'font ", 6"'
#     plot.xrange "['#{dates[0]}':'#{dates[-1]}']"
#     plot.yrange "[0:50]"
#     plot.title  "File Complexity Evolution"
#     plot.xlabel "Year"
#     plot.ylabel "File Complexity"
# 
#     
#     plot.data << Gnuplot::DataSet.new( [dates,values] ) do |ds|
#       ds.with = "lines"
#       ds.linewidth = 2
#       ds.using = '1:2'
#     end
#     
# #     plot.data << Gnuplot::DataSet.new( "cos(x)" ) do |ds|
# #       ds.with = "lines"
# #       ds.linewidth = 2
# #     end
#   end
  
#end
