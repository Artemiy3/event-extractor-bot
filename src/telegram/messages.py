START_MESSAGE = ('Hello! This is the event extractor bot.\n\n'
                 'Send text for extracting events in the next message. ⬇️')

HELP_MESSAGE = ('This bot is designed to extract events from text\\.\n\n'
                'An "event" is considered to be a construction that '
                'can answer the questions\\: \n'
                '*"Who?", "What?", "When?" and "Where?"*\\.\n\n'
                '*Example\\:* "John has sold a car in New York last Monday\\."\n'
                '*Who\\:* John,\n'
                '*Action\\:* sold a car,\n'
                '*When\\:* last Monday,\n'
                '*Where\\:* in New York\\.\n\n'
                'To test this out you can just send your text in a message'
                ' to the bot\\. ⬇️')

PROCESSING_MESSAGE = 'Processing your text...\n\nIt takes up to 10 seconds, please wait 🙏'