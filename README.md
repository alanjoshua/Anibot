# AniBot

<p> This is a simple discord bot that uses my simple Gogoanime scrapper to create a discord bot capable of functionality such as searching for anime, getting links to direct episodes, getting the link to the latest episode of an anime, and also scheduling automatic alerts for new episodes of an anime</p>

<br />
<br />
<br />

## Usage
<br />
<br />

<p> Searches for naruto on gogoanime, and outputs each result onto discord char</p> 
  
```!findAnime "naruto"```

<br />
<br />
<br />

<p> Get link to naruto episode 10</p>
<p> Here, "naruto" is the exact the anime title/link in Gogoanime. Other anime might have complicated titles, so first use !findAnime to get exact title</p>

```!getEpisode "naruto" 10```

<br />
<br />
<br />

<p> Get latest episode from naruto </p>

<p> This function uses selenium with chrome in headless mode, so make sure to have chromedrivers installed and added to system path </p>

```latest_episode = !latestAnime "naruto"```
<br />
<br />
<br />

<p> Create an alert for new episodes of naruto </p
  
 ``` !addAnimeAlert "naruto"```
 <br />
 
 <p> Create an alert for new episodes of naruto with a timeout of 1000 seconds (100 is the default) </p
  
  ``` !addAnimeAlert "naruto" 1000```
 <br />
 
  <p> Create an alert for new episodes of naruto with a timeout of 1000 seconds and send alerts to the channel "alerts" (By default, anime_alerts is the default channel) </p
  
  ``` !addAnimeAlert "naruto" 1000 "alerts" ```
 <br />
 
<br />
<br />
<br />

<p> Stop an alert </p

``` !stopAnimeAlert "naruto" ```
