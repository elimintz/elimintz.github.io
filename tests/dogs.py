from justpy import *

def dog_test(request):
    breeds = ['affenpinscher', 'african', 'airedale', 'akita', 'appenzeller', 'basenji', 'beagle', 'bluetick',
              'borzoi', 'bouvier', 'boxer', 'brabancon', 'briard', 'bulldog-boston', 'bulldog-french',
              'bullterrier-staffordshire', 'cairn', 'cattledog-australian', 'chihuahua', 'chow', 'clumber', 'cockapoo',
              'collie-border', 'coonhound', 'corgi-cardigan', 'cotondetulear', 'dachshund', 'dalmatian', 'dane-great',
              'deerhound-scottish', 'dhole', 'dingo', 'doberman', 'elkhound-norwegian', 'entlebucher', 'eskimo',
              'frise-bichon', 'germanshepherd', 'greyhound-italian', 'groenendael', 'hound-afghan', 'hound-basset',
              'hound-blood', 'hound-english', 'hound-ibizan', 'hound-walker', 'husky', 'keeshond', 'kelpie',
              'komondor', 'kuvasz', 'labrador', 'leonberg', 'lhasa', 'malamute', 'malinois', 'maltese', 'mastiff-bull',
              'mastiff-tibetan', 'mexicanhairless', 'mix', 'mountain-bernese', 'mountain-swiss', 'newfoundland',
              'otterhound', 'papillon', 'pekinese', 'pembroke', 'pinscher-miniature', 'pointer-german',
              'pointer-germanlonghair', 'pomeranian', 'poodle-miniature', 'poodle-standard', 'poodle-toy', 'pug',
              'puggle', 'pyrenees', 'redbone', 'retriever-chesapeake', 'retriever-curly', 'retriever-flatcoated',
              'retriever-golden', 'ridgeback-rhodesian', 'rottweiler', 'saluki', 'samoyed', 'schipperke',
              'schnauzer-giant', 'schnauzer-miniature', 'setter-english', 'setter-gordon', 'setter-irish',
              'sheepdog-english', 'sheepdog-shetland', 'shiba', 'shihtzu', 'spaniel-blenheim', 'spaniel-brittany',
              'spaniel-cocker', 'spaniel-irish', 'spaniel-japanese', 'spaniel-sussex', 'spaniel-welsh', 'springer-english',
              'stbernard', 'terrier-american', 'terrier-australian', 'terrier-bedlington', 'terrier-border',
              'terrier-dandie', 'terrier-fox', 'terrier-irish', 'terrier-kerryblue', 'terrier-lakeland', 'terrier-norfolk',
              'terrier-norwich', 'terrier-patterdale', 'terrier-russell', 'terrier-scottish', 'terrier-sealyham',
              'terrier-silky', 'terrier-tibetan', 'terrier-toy', 'terrier-westhighland', 'terrier-wheaten',
              'terrier-yorkshire', 'vizsla', 'weimaraner', 'whippet', 'wolfhound-irish']
    wp = QuasarPage()
    wp.body_style = 'overflow: hidden'
    bp = parse_html("""
    <div class="q-pa-md">
    <q-layout view="HHH lpr Fff" container  style="height: 95vh" class="shadow-2 rounded-borders">
        <q-header reveal class="bg-purple">
            <q-toolbar name="toolbar">
                <q-btn flat round dense icon="menu"/>
                <q-toolbar-title>Dog Pictures</q-toolbar-title>
                <q-btn glossy label="Next Picture" classes="q-mr-sm" name="next_picture"></q-btn>
            </q-toolbar>
        </q-header>
        <q-drawer name="drawer" width=300 breakpoint=700 show-if-above elevated content-class="bg-white text-blue">
            <q-scroll-area class="fit">
                <div class="q-pa-sm">
                    <q-list name="thumbnail_list">
                    </q-list>
                </div>
            </q-scroll-area>
        </q-drawer>
        <q-footer class="bg-purple text-white">
            <div class="text-white q-pa-xs" style="height: 30px;" name="footer"></div>
        </q-footer>
        <q-page-container style="overflow: hidden;">
            <q-page padding name="main_page" style="overflow: hidden;">
                    
                        <q-img src="https://images.dog.ceo/breeds/papillon/n02086910_6087.jpg" class="cursor-pointer" name="image" style="height: 400px; width: 700px">
                       <q-tooltip content-class="bg-purple" content-style="font-size: 13px" transition-show="scale" transition-hide="scale" anchor="top middle"  name="tooltip">
          Click image for next picture
        </q-tooltip>
                    </q-img>
            </q-page>
        </q-page-container>
    </q-layout>
</div>
    """, a=wp)
    main_image = bp.name_dict['image']
    l = Link(url='https://v1.quasar-framework.org/', text='Quasar', target='blank', classes="text-white")
    bp.name_dict['footer'].add(l)
    bp.name_dict['tooltip'].disable_events = True
    main_image.breed = 'papillon'
    breed_select = QBtnDropdown(auto_close=True, split=True, glossy=True, label='Select Breed', icon='fas fa-dog', a=bp.name_dict['toolbar'])
    breed_list = QList(separator=True, dense=True, a=breed_select)
    def change_breed(self, msg):
        main_image.breed = self.breed
        change_pic(main_image, msg)
        breed_select.label=self.breed

    for breed in breeds:
        breed_item_html = f'''<q-item clickable v-close-menu v-ripple>
                            <q-item-section >
                                <q-item-label>{breed}</q-item-label>
                            </q-item-section>
                        </q-item>'''
        # breed_item = parse_html(breed_item_html).first()
        breed_item = parse_html(breed_item_html)
        breed_item.breed = breed
        breed_item.on('click', change_breed)
        breed_list.add(breed_item)

    def add_thumbnail(self, msg):
        list_item_html = f'''<q-item clickable v-ripple>
                            <q-item-section thumbnail>
                                <img src="{self.src}"/>
                            </q-item-section>
                            <q-item-section>{self.breed}</q-item-section>
                            <q-item-section> <q-btn class="gt-xs text-grey-8" size="12px" flat dense round icon="delete" name="delete"/></q-item-section>
                        </q-item>'''
        list_item = parse_html(list_item_html)
        list_item.breed = self.breed
        list_item.src = self.src
        # list_item.delete = list_item.name_dict['delete']

        list_item.name_dict['delete'].list = bp.name_dict['thumbnail_list']
        list_item.name_dict['delete'].list_item = list_item
        bp.name_dict['thumbnail_list'].add(list_item)
        def display_thumbnail(self, msg):
            main_image.src = self.src

        list_item.on('mouseenter', display_thumbnail)
        def delete_list_item(self, msg):
            self.list.remove(self.list_item)
        list_item.name_dict['delete'].on('click',delete_list_item)


    def change_pic(self, msg):
        r = (requests.get(f'https://dog.ceo/api/breed/{self.breed}/images/random')).json()
        self.src = r['message']
        add_thumbnail(self, msg)


    def next_pic(self, msg):
        change_pic(main_image, msg)

    main_image.on('click', change_pic)
    bp.name_dict['next_picture'].on('click', next_pic)
    change_pic(main_image, {})
    return wp

justpy(dog_test)