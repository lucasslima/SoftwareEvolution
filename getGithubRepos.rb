require 'net/http'
require 'json'

NUMBER_OF_PAGES=9
PER_PAGE_PARAMETER='&per_page=100'
#Pega o nome da organização como primeiro argumento
ORGANIZATION=ARGV[0]
(1..NUMBER_OF_PAGES).each do |page|
  page_parameter="?page=#{page}"
  url = URI.parse("https://api.github.com/orgs/#{ORGANIZATION}/repos#{page_parameter}#{PER_PAGE_PARAMETER}")
  req = Net::HTTP::Get.new(url.to_s)
  res = Net::HTTP.start(url.host, url.port,
  :use_ssl => url.scheme == 'https') {|http|
    http.request(req)
  } 
  JSON.load(res.body).each do |repo|
    %x[git clone #{repo["clone_url"]}]
  end
end


# puts JSON.pretty_generate(res.body)
