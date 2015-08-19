var data = {
             champions: ["Aatrox", "Ahri", "Akali", "Alistar", "Anivia", "Amumu", "Annie", "Ashe", "Azir", "Bard", "Blitzcrank", "Brand", "Braum", "Caitlyn", "Cassiopeia", "Cho'Gath", "Corki", "Diana", "Dr. Mundo", "Draven", "Ekko", "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves", "Hecarim", "Heimerdinger", "Irelia", "Janna", "Jarvan IV", "Jax", "Jayce", "Jinx", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", "Kennen", "Kha'Zix", "Kog'Maw", "LeBlanc", "Lee Sin", "Leona", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", "Master Yi", "Miss Fortune", "Mordekaiser", "Morgana", "Nami", "Nasus", "Nautilus", "Nidalee", "Nocturne", "Nunu", "Olaf", "Orianna", "Pantheon", "Poppy", "Quinn", "Rammus", "Rek'Sai", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", "Sejuani", "Shaco", "Shen", "Shyvana", "Singed", "Sion", "Sivir", "Skarner", "Sona", "Soraka", "Swain", "Syndra", "Tahm Kench", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Trynadmere", "Twisted Fate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vi", "Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xerath", "Xin Zhao", "Yasuo", "Yorick", "Zac", "Zed", "Ziggs", "Zilean"],
            items: ["Abyssal Scepter", "Aegis of the Legion", "Archangel's Staff", "Ardent Censer", "Athene's Unholy Grail", "Banner of Command", "Banshee's Veil", "Berserker's Greaves", "Blade of the Ruined King", "Boots of Mobility", "Boots of Swiftness", "Chalice of Harmony", "Dead Man's Plate", "Frost Queen's Claim", "Frozen Heart", "Frozen Mallet", "Guardian Angel", "Hexdrinker", "Haunting Guise", "Ionian Boots of Lucidity", "Iceborn Gauntlet", "Last Whisper", "Liandry's Torment", "Lich Bane", "Luden's Echo", "Madred's Razors", "Manamune", "Mejai's Soulstealer", "Mercury's Treads", "Mikael's Crcucible", "Morellonomicon", "Muramana", "Ohmwrecker", "Quicksilver Sash", "Rabadon's Deathcap", "Righteous Glory", "Rod of Ages", "Runaan's Hurrican", "Rylai's Crystal Scepter", "Seraph's Embrace", "Sightstone", "Sunfire Cape", "Tear of the Goddess", "The Bloodthirster", "The Brutalizer", "Thornmail", "Twin Shadows", "Warmog's Armor", "Will of the Ancients", "Youmuu's Ghostblade", "Zeke's Harbringer", "Zhonya's Hourglass"]
        };

        $('#q').typeahead({
            minLength: 1,
            order: "asc",
            group: true,
            groupMaxItem: 3,
            hint: true,
            dropdownFilter: "All",
            href: "https://en.wikipedia.org/?title={{display}}",
            template: "{{display}}, <small><em>{{group}}</em></small>",
            source: {
                champion: {
                    data: data.champions
                },
                item: {
                    data: data.items
                }
            },
            callback: {
                onClickAfter: function (node, a, item, event) {

                    var r = confirm("You will be redirected to:\n" + item.href + "\n\nContinue?");
                    if (r == true) {
                        window.open(item.href);
                    }

                    $('#result-container').text('');

                }
            },
            debug: true
        });