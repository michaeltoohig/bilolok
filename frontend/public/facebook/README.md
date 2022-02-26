# Facebook bot endpoint

This sucks, really. Facebook crawler is such a PITA and requires specialized care to work correctly so we have to have this special folder to handle its requests.

## But Why?

Facebook bot does not follow any redirects what so ever, meaning it will not following our http -> https redirect and always attempts to access the insecure http endpoint first. So we have to have this special case to support their nonsense since so much of our target audience are Facebook users.

## Known Issues

This solution requires maintaining *another* copy of the Open Graph tags independent from whatever is written to the initial `public/index.html` file and whatever is dynamically updated via `vue-meta`. That is **3** sources of truth to remember and maintain which I know is a problem but have no obvious solution for yet. I accept this only because I need a solution now as I have begun sharing the app on social media and want a good experience for Facebook users in the short term.

Also, this is another static solution, meaning the values of the Open Graph tags we select will not change regardless of the full URL path visted by the bot.

## Possible Solutions

We could host a small Flask or Starlette app in our existing app that listens on a different port or endpoint then dynamically sets the OG tags based on the endpoint being visited. This could mean we correctly show the name of the nakamal and the latest image of that nakamal if the URL to the nakamal is shared on social media. It still means `vue-meta` has to be kept in sync with this possible solution in terms of content.

I do kind of like this solution though because it could grow into a "mobile" version of the app for slow devices by only rendering basic HTML files minus the complex SPA overhead.

The best solution if time/energy is available would be to migrate to a server-side rendered Vue app which would mean `vue-meta` becomes the only source of truth for Open Graph tags