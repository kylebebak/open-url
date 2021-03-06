# Open URL opens selected URLs, files, folders, or looks up text in web searcher

import sublime
import sublime_plugin

import webbrowser
import urllib
import urllib.parse
import threading
import re
import os
import subprocess
import platform


class OpenUrlCommand(sublime_plugin.TextCommand):

    # list of known domains for short urls, like ironcowboy.co
    domains = "AAA|AARP|ABB|ABBOTT|ABBVIE|ABOGADO|ABUDHABI|AC|ACADEMY|ACCENTURE|ACCOUNTANT|ACCOUNTANTS|ACO|ACTIVE|ACTOR|AD|ADAC|ADS|ADULT|AE|AEG|AERO|AF|AFL|AG|AGAKHAN|AGENCY|AI|AIG|AIRFORCE|AIRTEL|AKDN|AL|ALIBABA|ALIPAY|ALLFINANZ|ALLY|ALSACE|AM|AMICA|AMSTERDAM|ANALYTICS|ANDROID|ANQUAN|AO|APARTMENTS|APP|APPLE|AQ|AQUARELLE|AR|ARAMCO|ARCHI|ARMY|ARPA|ARTE|AS|ASIA|ASSOCIATES|AT|ATTORNEY|AU|AUCTION|AUDI|AUDIO|AUTHOR|AUTO|AUTOS|AVIANCA|AW|AWS|AX|AXA|AZ|AZURE|BA|BABY|BAIDU|BAND|BANK|BAR|BARCELONA|BARCLAYCARD|BARCLAYS|BAREFOOT|BARGAINS|BAUHAUS|BAYERN|BB|BBC|BBVA|BCG|BCN|BD|BE|BEATS|BEER|BENTLEY|BERLIN|BEST|BET|BF|BG|BH|BHARTI|BI|BIBLE|BID|BIKE|BING|BINGO|BIO|BIZ|BJ|BLACK|BLACKFRIDAY|BLOOMBERG|BLUE|BM|BMS|BMW|BN|BNL|BNPPARIBAS|BO|BOATS|BOEHRINGER|BOM|BOND|BOO|BOOK|BOOTS|BOSCH|BOSTIK|BOT|BOUTIQUE|BR|BRADESCO|BRIDGESTONE|BROADWAY|BROKER|BROTHER|BRUSSELS|BS|BT|BUDAPEST|BUGATTI|BUILD|BUILDERS|BUSINESS|BUY|BUZZ|BV|BW|BY|BZ|BZH|CA|CAB|CAFE|CAL|CALL|CAMERA|CAMP|CANCERRESEARCH|CANON|CAPETOWN|CAPITAL|CAR|CARAVAN|CARDS|CARE|CAREER|CAREERS|CARS|CARTIER|CASA|CASH|CASINO|CAT|CATERING|CBA|CBN|CC|CD|CEB|CENTER|CEO|CERN|CF|CFA|CFD|CG|CH|CHANEL|CHANNEL|CHASE|CHAT|CHEAP|CHLOE|CHRISTMAS|CHROME|CHURCH|CI|CIPRIANI|CIRCLE|CISCO|CITIC|CITY|CITYEATS|CK|CL|CLAIMS|CLEANING|CLICK|CLINIC|CLINIQUE|CLOTHING|CLOUD|CLUB|CLUBMED|CM|CN|CO|COACH|CODES|COFFEE|COLLEGE|COLOGNE|COM|COMMBANK|COMMUNITY|COMPANY|COMPARE|COMPUTER|COMSEC|CONDOS|CONSTRUCTION|CONSULTING|CONTACT|CONTRACTORS|COOKING|COOL|COOP|CORSICA|COUNTRY|COUPON|COUPONS|COURSES|CR|CREDIT|CREDITCARD|CREDITUNION|CRICKET|CROWN|CRS|CRUISES|CSC|CU|CUISINELLA|CV|CW|CX|CY|CYMRU|CYOU|CZ|DABUR|DAD|DANCE|DATE|DATING|DATSUN|DAY|DCLK|DDS|DE|DEALER|DEALS|DEGREE|DELIVERY|DELL|DELOITTE|DELTA|DEMOCRAT|DENTAL|DENTIST|DESI|DESIGN|DEV|DIAMONDS|DIET|DIGITAL|DIRECT|DIRECTORY|DISCOUNT|DJ|DK|DM|DNP|DO|DOCS|DOG|DOHA|DOMAINS|DOWNLOAD|DRIVE|DUBAI|DURBAN|DVAG|DZ|EARTH|EAT|EC|EDEKA|EDU|EDUCATION|EE|EG|EMAIL|EMERCK|ENERGY|ENGINEER|ENGINEERING|ENTERPRISES|EPSON|EQUIPMENT|ER|ERNI|ES|ESQ|ESTATE|ET|EU|EUROVISION|EUS|EVENTS|EVERBANK|EXCHANGE|EXPERT|EXPOSED|EXPRESS|EXTRASPACE|FAGE|FAIL|FAIRWINDS|FAITH|FAMILY|FAN|FANS|FARM|FASHION|FAST|FEEDBACK|FERRERO|FI|FILM|FINAL|FINANCE|FINANCIAL|FIRESTONE|FIRMDALE|FISH|FISHING|FIT|FITNESS|FJ|FK|FLICKR|FLIGHTS|FLIR|FLORIST|FLOWERS|FLSMIDTH|FLY|FM|FO|FOO|FOOTBALL|FORD|FOREX|FORSALE|FORUM|FOUNDATION|FOX|FR|FRESENIUS|FRL|FROGANS|FRONTIER|FTR|FUND|FURNITURE|FUTBOL|FYI|GA|GAL|GALLERY|GALLO|GALLUP|GAME|GARDEN|GB|GBIZ|GD|GDN|GE|GEA|GENT|GENTING|GF|GG|GGEE|GH|GI|GIFT|GIFTS|GIVES|GIVING|GL|GLASS|GLE|GLOBAL|GLOBO|GM|GMAIL|GMBH|GMO|GMX|GN|GOLD|GOLDPOINT|GOLF|GOO|GOOG|GOOGLE|GOP|GOT|GOV|GP|GQ|GR|GRAINGER|GRAPHICS|GRATIS|GREEN|GRIPE|GROUP|GS|GT|GU|GUARDIAN|GUCCI|GUGE|GUIDE|GUITARS|GURU|GW|GY|HAMBURG|HANGOUT|HAUS|HDFCBANK|HEALTH|HEALTHCARE|HELP|HELSINKI|HERE|HERMES|HIPHOP|HITACHI|HIV|HK|HKT|HM|HN|HOCKEY|HOLDINGS|HOLIDAY|HOMEDEPOT|HOMES|HONDA|HORSE|HOST|HOSTING|HOTELES|HOTMAIL|HOUSE|HOW|HR|HSBC|HT|HTC|HU|HYUNDAI|IBM|ICBC|ICE|ICU|ID|IE|IFM|IINET|IL|IM|IMAMAT|IMMO|IMMOBILIEN|IN|INDUSTRIES|INFINITI|INFO|ING|INK|INSTITUTE|INSURANCE|INSURE|INT|INTERNATIONAL|INVESTMENTS|IO|IPIRANGA|IQ|IR|IRISH|IS|ISELECT|ISMAILI|IST|ISTANBUL|IT|ITAU|IWC|JAGUAR|JAVA|JCB|JCP|JE|JETZT|JEWELRY|JLC|JLL|JM|JMP|JNJ|JO|JOBS|JOBURG|JOT|JOY|JP|JPMORGAN|JPRS|JUEGOS|KAUFEN|KDDI|KE|KERRYHOTELS|KERRYLOGISTICS|KERRYPROPERTIES|KFH|KG|KH|KI|KIA|KIM|KINDER|KITCHEN|KIWI|KM|KN|KOELN|KOMATSU|KP|KPMG|KPN|KR|KRD|KRED|KUOKGROUP|KW|KY|KYOTO|KZ|LA|LACAIXA|LAMBORGHINI|LAMER|LANCASTER|LAND|LANDROVER|LANXESS|LASALLE|LAT|LATROBE|LAW|LAWYER|LB|LC|LDS|LEASE|LECLERC|LEGAL|LEXUS|LGBT|LI|LIAISON|LIDL|LIFE|LIFEINSURANCE|LIFESTYLE|LIGHTING|LIKE|LIMITED|LIMO|LINCOLN|LINDE|LINK|LIPSY|LIVE|LIVING|LIXIL|LK|LOAN|LOANS|LOCUS|LOL|LONDON|LOTTE|LOTTO|LOVE|LR|LS|LT|LTD|LTDA|LU|LUPIN|LUXE|LUXURY|LV|LY|MA|MADRID|MAIF|MAISON|MAKEUP|MAN|MANAGEMENT|MANGO|MARKET|MARKETING|MARKETS|MARRIOTT|MBA|MC|MD|ME|MED|MEDIA|MEET|MELBOURNE|MEME|MEMORIAL|MEN|MENU|MEO|METLIFE|MG|MH|MIAMI|MICROSOFT|MIL|MINI|MK|ML|MLS|MM|MMA|MN|MO|MOBI|MOBILY|MODA|MOE|MOI|MOM|MONASH|MONEY|MONTBLANC|MORMON|MORTGAGE|MOSCOW|MOTORCYCLES|MOV|MOVIE|MOVISTAR|MP|MQ|MR|MS|MT|MTN|MTPC|MTR|MU|MUSEUM|MUTUAL|MUTUELLE|MV|MW|MX|MY|MZ|NA|NADEX|NAGOYA|NAME|NATURA|NAVY|NC|NE|NEC|NET|NETBANK|NETWORK|NEUSTAR|NEW|NEWS|NEXT|NEXTDIRECT|NEXUS|NF|NG|NGO|NHK|NI|NICO|NIKON|NINJA|NISSAN|NISSAY|NL|NO|NOKIA|NORTHWESTERNMUTUAL|NORTON|NOWRUZ|NOWTV|NP|NR|NRA|NRW|NTT|NU|NYC|NZ|OBI|OFFICE|OKINAWA|OLAYAN|OLAYANGROUP|OM|OMEGA|ONE|ONG|ONL|ONLINE|OOO|ORACLE|ORANGE|ORG|ORGANIC|ORIGINS|OSAKA|OTSUKA|OVH|PA|PAGE|PAMPEREDCHEF|PANERAI|PARIS|PARS|PARTNERS|PARTS|PARTY|PASSAGENS|PCCW|PE|PET|PF|PG|PH|PHARMACY|PHILIPS|PHOTO|PHOTOGRAPHY|PHOTOS|PHYSIO|PIAGET|PICS|PICTET|PICTURES|PID|PIN|PING|PINK|PIZZA|PK|PL|PLACE|PLAY|PLAYSTATION|PLUMBING|PLUS|PM|PN|POHL|POKER|PORN|POST|PR|PRAXI|PRESS|PRO|PROD|PRODUCTIONS|PROF|PROGRESSIVE|PROMO|PROPERTIES|PROPERTY|PROTECTION|PS|PT|PUB|PW|PWC|PY|QA|QPON|QUEBEC|QUEST|RACING|RE|READ|REALTOR|REALTY|RECIPES|RED|REDSTONE|REDUMBRELLA|REHAB|REISE|REISEN|REIT|REN|RENT|RENTALS|REPAIR|REPORT|REPUBLICAN|REST|RESTAURANT|REVIEW|REVIEWS|REXROTH|RICH|RICHARDLI|RICOH|RIO|RIP|RO|ROCHER|ROCKS|RODEO|ROOM|RS|RSVP|RU|RUHR|RUN|RW|RWE|RYUKYU|SA|SAARLAND|SAFE|SAFETY|SAKURA|SALE|SALON|SAMSUNG|SANDVIK|SANDVIKCOROMANT|SANOFI|SAP|SAPO|SARL|SAS|SAXO|SB|SBI|SBS|SC|SCA|SCB|SCHAEFFLER|SCHMIDT|SCHOLARSHIPS|SCHOOL|SCHULE|SCHWARZ|SCIENCE|SCOR|SCOT|SD|SE|SEAT|SECURITY|SEEK|SELECT|SENER|SERVICES|SEVEN|SEW|SEX|SEXY|SFR|SG|SH|SHARP|SHAW|SHELL|SHIA|SHIKSHA|SHOES|SHOUJI|SHOW|SHRIRAM|SI|SINA|SINGLES|SITE|SJ|SK|SKI|SKIN|SKY|SKYPE|SL|SM|SMILE|SN|SNCF|SO|SOCCER|SOCIAL|SOFTBANK|SOFTWARE|SOHU|SOLAR|SOLUTIONS|SONG|SONY|SOY|SPACE|SPIEGEL|SPOT|SPREADBETTING|SR|SRL|ST|STADA|STAR|STARHUB|STATEBANK|STATEFARM|STATOIL|STC|STCGROUP|STOCKHOLM|STORAGE|STORE|STREAM|STUDIO|STUDY|STYLE|SU|SUCKS|SUPPLIES|SUPPLY|SUPPORT|SURF|SURGERY|SUZUKI|SV|SWATCH|SWISS|SX|SY|SYDNEY|SYMANTEC|SYSTEMS|SZ|TAB|TAIPEI|TALK|TAOBAO|TATAMOTORS|TATAR|TATTOO|TAX|TAXI|TC|TCI|TD|TEAM|TECH|TECHNOLOGY|TEL|TELECITY|TELEFONICA|TEMASEK|TENNIS|TEVA|TF|TG|TH|THD|THEATER|THEATRE|TICKETS|TIENDA|TIFFANY|TIPS|TIRES|TIROL|TJ|TK|TL|TM|TMALL|TN|TO|TODAY|TOKYO|TOOLS|TOP|TORAY|TOSHIBA|TOTAL|TOURS|TOWN|TOYOTA|TOYS|TR|TRADE|TRADING|TRAINING|TRAVEL|TRAVELERS|TRAVELERSINSURANCE|TRUST|TRV|TT|TUBE|TUI|TUNES|TUSHU|TV|TVS|TW|TZ|UA|UBS|UG|UK|UNICOM|UNIVERSITY|UNO|UOL|US|UY|UZ|VA|VACATIONS|VANA|VC|VE|VEGAS|VENTURES|VERISIGN|VERSICHERUNG|VET|VG|VI|VIAJES|VIDEO|VIG|VIKING|VILLAS|VIN|VIP|VIRGIN|VISION|VISTA|VISTAPRINT|VIVA|VLAANDEREN|VN|VODKA|VOLKSWAGEN|VOTE|VOTING|VOTO|VOYAGE|VU|VUELOS|WALES|WALTER|WANG|WANGGOU|WARMAN|WATCH|WATCHES|WEATHER|WEATHERCHANNEL|WEBCAM|WEBER|WEBSITE|WED|WEDDING|WEIBO|WEIR|WF|WHOSWHO|WIEN|WIKI|WILLIAMHILL|WIN|WINDOWS|WINE|WME|WOLTERSKLUWER|WORK|WORKS|WORLD|WS|WTC|WTF|XBOX|XEROX|XIHUAN|XIN|XN--11B4C3D|XN--1CK2E1B|XN--1QQW23A|XN--30RR7Y|XN--3BST00M|XN--3DS443G|XN--3E0B707E|XN--3PXU8K|XN--42C2D9A|XN--45BRJ9C|XN--45Q11C|XN--4GBRIM|XN--55QW42G|XN--55QX5D|XN--5TZM5G|XN--6FRZ82G|XN--6QQ986B3XL|XN--80ADXHKS|XN--80AO21A|XN--80ASEHDB|XN--80ASWG|XN--8Y0A063A|XN--90A3AC|XN--90AIS|XN--9DBQ2A|XN--9ET52U|XN--9KRT00A|XN--B4W605FERD|XN--BCK1B9A5DRE4C|XN--C1AVG|XN--C2BR7G|XN--CCK2B3B|XN--CG4BKI|XN--CLCHC0EA0B2G2A9GCD|XN--CZR694B|XN--CZRS0T|XN--CZRU2D|XN--D1ACJ3B|XN--D1ALF|XN--E1A4C|XN--ECKVDTC9D|XN--EFVY88H|XN--ESTV75G|XN--FCT429K|XN--FHBEI|XN--FIQ228C5HS|XN--FIQ64B|XN--FIQS8S|XN--FIQZ9S|XN--FJQ720A|XN--FLW351E|XN--FPCRJ9C3D|XN--FZC2C9E2C|XN--FZYS8D69UVGM|XN--G2XX48C|XN--GCKR3F0F|XN--GECRJ9C|XN--H2BRJ9C|XN--HXT814E|XN--I1B6B1A6A2E|XN--IMR513N|XN--IO0A7I|XN--J1AEF|XN--J1AMH|XN--J6W193G|XN--JLQ61U9W7B|XN--JVR189M|XN--KCRX77D1X4A|XN--KPRW13D|XN--KPRY57D|XN--KPU716F|XN--KPUT3I|XN--L1ACC|XN--LGBBAT1AD8J|XN--MGB9AWBF|XN--MGBA3A3EJT|XN--MGBA3A4F16A|XN--MGBA7C0BBN0A|XN--MGBAAM7A8H|XN--MGBAB2BD|XN--MGBAYH7GPA|XN--MGBB9FBPOB|XN--MGBBH1A71E|XN--MGBC0A9AZCG|XN--MGBCA7DZDO|XN--MGBERP4A5D4AR|XN--MGBPL2FH|XN--MGBT3DHD|XN--MGBTX2B|XN--MGBX4CD0AB|XN--MIX891F|XN--MK1BU44C|XN--MXTQ1M|XN--NGBC5AZD|XN--NGBE9E0A|XN--NODE|XN--NQV7F|XN--NQV7FS00EMA|XN--NYQY26A|XN--O3CW4H|XN--OGBPF8FL|XN--P1ACF|XN--P1AI|XN--PBT977C|XN--PGBS0DH|XN--PSSY2U|XN--Q9JYB4C|XN--QCKA1PMC|XN--QXAM|XN--RHQV96G|XN--ROVU88B|XN--S9BRJ9C|XN--SES554G|XN--T60B56A|XN--TCKWE|XN--UNUP4Y|XN--VERMGENSBERATER-CTB|XN--VERMGENSBERATUNG-PWB|XN--VHQUV|XN--VUQ861B|XN--W4R85EL8FHU5DNRA|XN--W4RS40L|XN--WGBH1C|XN--WGBL6A|XN--XHQ521B|XN--XKC2AL3HYE2A|XN--XKC2DL3A5EE0H|XN--Y9A3AQ|XN--YFRO4I67O|XN--YGBI2AMMX|XN--ZFR164B|XPERIA|XXX|XYZ|YACHTS|YAHOO|YAMAXUN|YANDEX|YE|YODOBASHI|YOGA|YOKOHAMA|YOU|YOUTUBE|YT|YUN|ZA|ZARA|ZERO|ZIP|ZM|ZONE|ZUERICH|ZW"

    def run(self, edit=None, url=None):
        self.config = sublime.load_settings("open_url.sublime-settings")

        # sublime text has its own open_url command used for things like Help menu > Documentation
        # so if a url is specified, then open it instead of getting text from the edit window
        if url is None:
            url = self.selection()

        # expand variables in the path
        url = os.path.expandvars(url)

        # strip quotes if quoted
        if (url.startswith("\"") & url.endswith("\"")) | (url.startswith("\'") & url.endswith("\'")):
            url = url[1:-1]

        try:
            # treat url as path relative to open view
            absolute_path = os.path.normpath(os.path.join(os.path.dirname(self.view.file_name()), url))
        except (TypeError, AttributeError):
            # if open view has never been saved, treat url as path relative to project root
            absolute_path = self.path_relative_to_project_root(url)
        else:
            # if open view has been saved but path relative to open view doesn't exist,
            # fall back to path relative to project root
            if not os.path.exists(absolute_path):
                absolute_path = self.path_relative_to_project_root(url)

        # if this is a directory, show it (absolute or relative)
        # if it is a path to a file, open the file in sublime (absolute or relative)
        # if it is a URL, open in browser
        # otherwise google it
        if os.path.isdir(url):
            self.folder_action(url)

        if os.path.isdir(os.path.expanduser(url)):
            self.folder_action(os.path.expanduser(url))

        elif absolute_path and os.path.isdir(absolute_path):
            self.folder_action(absolute_path)

        elif os.path.exists(url):
            self.choose_action(url)

        elif os.path.exists(os.path.expandvars(url)):
            self.choose_action(os.path.expandvars(url))

        elif os.name == 'posix' and os.path.exists(os.path.expanduser(url)):
            self.choose_action(os.path.expanduser(url))

        elif absolute_path and os.path.exists(absolute_path):
            self.choose_action(absolute_path)

        else:
            if "://" in url:
                webbrowser.open_new_tab(url)
            elif re.search(r"\w[^\s]*\.(?:%s)[^\s]*\Z" % self.domains, url, re.IGNORECASE):
                if "://" not in url:
                    url = "http://" + url
                webbrowser.open_new_tab(url)
            else:
                self.modify_search_or_web_search_action(url)

    def path_relative_to_project_root(self, url):
        project = self.view.window().project_data()
        if project is not None:
            try:
                return "{}/{}".format(project['folders'][0]['path'], url)
            except (KeyError, IndexError):
                return None
        else:
            return None

    # pulls the current selection or url under the cursor
    def selection(self):
        s = self.view.sel()[0]

        # expand selection to possible URL
        start = s.a
        end = s.b

        # if nothing is selected, expand selection to nearest terminators
        if (start == end):
            view_size = self.view.size()
            terminator = list(self.config.get('terminators'))

            # move the selection back to the start of the url
            while (start > 0
                    and not self.view.substr(start - 1) in terminator
                    and self.view.classify(start) & sublime.CLASS_LINE_START == 0):
                start -= 1

            # move end of selection forward to the end of the url
            while (end < view_size
                    and not self.view.substr(end) in terminator
                    and self.view.classify(end) & sublime.CLASS_LINE_END == 0):
                end += 1

        # grab the URL
        return self.view.substr(sublime.Region(start, end)).strip()

    # for files, as the user if they's like to edit or run the file
    def choose_action(self, path):
        action = 'menu'
        autoinfo = None

        # see if there's already an action defined for this file
        for auto in self.config.get('autoactions'):
            # see if this line applies to this opperating system
            if 'os' in auto:
                oscheck = auto['os'] == 'any' \
                    or (auto['os'] == 'win' and platform.system() == 'Windows') \
                    or (auto['os'] == 'lnx' and platform.system() == 'Linux') \
                    or (auto['os'] == 'mac' and platform.system() == 'Darwin') \
                    or (auto['os'] == 'psx' and (platform.system() == 'Darwin' or platform.system() == 'Linux'))
            else:
                oscheck = True

            # if the line is for this OS, then check to see if we have a file pattern match
            if oscheck:
                for ending in auto['endswith']:
                    if (path.endswith(ending)):
                        action = auto['action']
                        autoinfo = auto
                        break

        # either show a menu or perform the action
        if action == 'menu':
            sublime.active_window().show_quick_panel(
                ["edit", "run", "reveal", "new window", "system open"],
                lambda idx: self.select_done(idx, autoinfo, path)
            )
        elif action == 'edit':
            self.select_done(0, autoinfo, path)
        elif action == 'run':
            self.select_done(1, autoinfo, path)
        else:
            raise 'unsupported action'

    def folder_action(self, folder):
        openers = self.config.get('directory_open_commands', {})
        opts = ["reveal", "add to project", "new window"] + [opener.get('label') for opener in openers]
        sublime.active_window().show_quick_panel(opts, lambda idx: self.folder_done(idx, opts, folder))

    def folder_done(self, idx, opts, folder):
        if idx < 0:
            return
        if idx == 0:
            self.reveal(folder)
        elif idx == 1:
            # add folder to project
            d = self.view.window().project_data()
            if not d:
                d = {}
            if 'folders' not in d:
                d['folders'] = []
            d['folders'].append({'path': folder})
            self.view.window().set_project_data(d)
        elif idx == 2:
            self.open_in_new_window(folder)

        else:  # custom directory opener was used
            openers = self.config.get('directory_open_commands', {})
            idx = idx - 3
            commands = openers[idx].get('commands')
            subprocess.check_call(commands + [folder])

    def modify_search_or_web_search_action(self, term):
        searchers = self.config.get('web_searchers')
        opts = ['modify url']
        urls = ['']
        opts += [s['label'] for s in searchers]
        urls += [s['url'] for s in searchers]
        sublime.active_window().show_quick_panel(opts, lambda idx: self.web_search_done(idx, urls, term))

    def web_search_done(self, idx, urls, term):
        if idx == 0:
            self.view.window().show_input_panel('URL or path:', term, self.url_search_modified, None, None)
        elif idx > 0:
            webbrowser.open_new_tab("{}{}".format(urls[idx], term))

    def url_search_modified(self, text):
        """Call `open_url` again on modified path.
        """
        try:
            self.view.run_command('open_url', {'url': text})
        except ValueError:
            pass

    def reveal(self, path):
        spec = {'dir': {'Darwin': ['open'], 'Windows': ['explorer'], 'Linux': ['nautilus', '--browser']}, 'file': {'Darwin': ['open', '-R'], 'Windows': ['explorer', '/select,"<path>"'], 'Linux': ['nautilus', '--browser']}}
        if not platform.system() in spec['dir']:
            raise 'unsupported os'
        args = spec['dir' if os.path.isdir(path) else 'file'][platform.system()]
        if '<path>' in args[-1:]:
            args[-1:] = args[-1:].replace('<path>', path)
        else:
            args.append(path)
        subprocess.Popen(args)

    # shell execution must be on another thread to keep Sublime from locking if it's a sublime file
    def callsubproc(self, args, shell):
        subprocess.call(args, shell=shell)

    # run using a seperate thread
    def runapp(self, args, shell=None):
        if shell is None:
            shell = not isinstance(args, list)
        threading.Thread(target=self.callsubproc, args=(args, shell)).start()

    def runfile(self, autoinfo, path):
        plat = platform.system()

        # default methods to open files
        defrun = {'Darwin': 'open', 'Windows': '', 'Linux': 'mimeopen'}
        if plat not in defrun:
            raise 'unsupported os'

        # check if there are special instructions to open this file
        if autoinfo is None or 'openwith' not in autoinfo:
            if autoinfo is not None and plat == 'Darwin' and 'app' in autoinfo:
                cmd = "%s -a %s %s" % self.quote((defrun[plat], autoinfo['app'], path))
            elif defrun[platform.system()]:
                cmd = "%s %s" % self.quote((defrun[platform.system()], path))
            else:
                cmd = self.quote(path)
        else:
            cmd = "%s %s" % self.quote((autoinfo['openwith'], path))

        # run command in a terminal and pause if desired
        if autoinfo and 'terminal' in autoinfo and autoinfo['terminal']:
            pause = 'pause' in autoinfo and autoinfo['pause']
            xterm = {'Darwin': '/opt/X11/bin/xterm', 'Linux': '/usr/bin/xterm'}
            if plat in xterm:
                cmd = [xterm[plat], '-e', cmd + ('; read -p "Press [ENTER] to continue..."' if pause else '')]
            elif os.name == 'nt':
                # subprocess.call has an odd behavior on windows in that if a parameter contains quotes
                # it tries to escape the quotes by adding a slash in front of each double quote
                # so c:\temp\hello.bat if passed to subprocess.call as "c:\temp\hello.bat" will be passed to the OS as \"c:\temp\hello.bat\"
                # echo Windows doesn't know how to interprit that, so we need to remove the double quotes,
                # which breaks files with spaces in their path
                cmd = ['c:\\windows\\system32\\cmd.exe', '/c', '%s%s' % (cmd.replace('"', ''), ' & pause' if pause else '')]
            else:
                raise 'unsupported os'

        # open the file on a seperate thread
        self.runapp(cmd)

    # for files, either open the file for editing in sublime, or shell execute the file
    def select_done(self, idx, autoinfo, path):
        if idx == 0:
            self.view.window().open_file(path)
        elif idx == 1:
            self.runfile(autoinfo, path)
        elif idx == 2:
            self.reveal(path)
        elif idx == 3:
            self.open_in_new_window(path)
        elif idx == 4:
            self.system_open(path)

    def system_open(self, path):
        if sublime.platform() == "osx":
            args = ['open', path]
        elif sublime.platform() == "linux":
            args = [path]
        elif sublime.platform() == "windows":
            args = ['start', path]
        else:
            raise Exception("unsupported os")
        subprocess.Popen(args, cwd=os.path.dirname(path))

    def quote(self, stuff):
        if isinstance(stuff, str):
            return '"' + stuff + '"'
        elif isinstance(stuff, list):
            return [self.quote(x) for x in stuff]
        elif isinstance(stuff, tuple):
            return tuple(self.quote(list(stuff)))
        else:
            raise 'unsupported type'

    def open_in_new_window(self, path):
        items = []

        executable_path = sublime.executable_path()

        if sublime.platform() == 'osx':
            app_path = executable_path[:executable_path.rfind(".app/")+5]
            executable_path = app_path+"Contents/SharedSupport/bin/subl"

        # build arguments
        path = os.path.abspath(path)
        items.append(executable_path)
        if os.path.isfile(path):
            items.append(os.path.dirname(path))
        items.append(path)

        subprocess.Popen(items, cwd=items[1])
