# -*- coding: utf-8 -*-
"""Build spec.json for DOC021 run02 attempt-01 (authoring aid, content authored manually)."""
import json
from pathlib import Path

A = Path(__file__).resolve().parents[1]
doc = json.loads((A / "source/DOC021.json").read_text(encoding="utf-8"))
T = {t["source_id"]: t["text"] for t in doc["turns"]}


def q(sid, text):
    assert text in T[sid], (sid, text)
    assert T[sid].count(text) == 1, (sid, text, T[sid].count(text))
    return {"source_id": sid, "quote": text, "role": "basis"}


Q = {
    "relocate": q("DOC021:T003", "Mainly when I move to a new neighborhood or to a new country, I need to find a new place. So I usually search on the Internet and use this type of web apps."),
    "choose_area": q("DOC021:T005", "So usually I choose a neighborhood or a place where I want to find a house in, and then I start searching by such keywords"),
    "keywords": q("DOC021:T005", "I start searching by such keywords to find relevant websites for that specific area"),
    "popular_sites": q("DOC021:T005", "I want to be familiar with which websites are the most popular or most used there."),
    "clustered": q("DOC021:T007", "Sometimes there are options that fits my budget and fits my requirements more clustered in specific neighborhoods"),
    "ask_locals": q("DOC021:T007", "asking people who lives, for example in that country, if they have any recommendation for the places"),
    "near_job": q("DOC021:T007", "if I have a specific job, or if I'm studying at specific college, I will usually pick a neighborhood that's close to that area"),
    "size_budget": q("DOC021:T009", "I will search by like the size of the place, or sometimes by bedroom counts. and with also a budget limit"),
    "secondary": q("DOC021:T009", "I can start filtering it down, using other non very important criteria, such as if they have, like some amenities"),
    "contact": q("DOC021:T011", "I'll start with the communication process, which will help me also to narrow down my options"),
    "reply_speed": q("DOC021:T011", "sometimes like how fast they will reply might affect my choices"),
    "research_name": q("DOC021:T013", "So I might just research by the if their place has some name."),
    "other_methods": q("DOC021:T013", "I'll try to communicate with them using other methods like email or phone."),
    "bad_sign": q("DOC021:T013", "It's just a bad sign that the management is not very good"),
    "no_response_q": q("DOC021:T012", "What do you typically do if you reach out to someone? But they don't respond to you."),
    "discover_only": q("DOC021:T017", "I mainly use this type of platforms like as a way to discover places."),
    "outside_apps": q("DOC021:T017", "I actually usually proceed with different type of communication outside of these apps."),
    "last_upd_complaint": q("DOC021:T019", "You don't know when was the time the information was lastly updated."),
    "long_form": q("DOC021:T019", "you will have this long form that you don't know how it will be submitted"),
    "short_comm": q("DOC021:T019", "You don't feel like you can communicate like in a short way."),
    "timeline": q("DOC021:T021", "a small visual of the timeline that, like the website, can show me what are the next steps. If I fail, therefore, what should I expect?"),
    "trust_enthusiasm": q("DOC021:T021", "it gives you more trust, and it gives you more enthusiasm to go through the process"),
    "last_upd_vision": q("DOC021:T021", "if I can see, like the information was last updated, for example, a week ago or 2 months ago"),
    "just_communicate": q("DOC021:T023", "You just want to communicate, to know more or to get specific information. Sometimes you don't want to write a custom message."),
    "required_fields": q("DOC021:T023", "all of them are required fields"),
    "skip_request": q("DOC021:T023", "So it makes me just get the information from the website and skip the process of requesting it through the website."),
    "three_units": q("DOC021:T025", "if there is like 3 apartments. With these specifications they can just list it with their specification, and I can have something similar to the concept of. Add to cart"),
    "what_next": q("DOC021:T025", "I would love like to know if I just proceeded with this option, what will happen when they would they respond to me? What will be next?"),
    "deterministic": q("DOC021:T025", "this a sort of visibility, and like deterministic steps, will make me more happy to to engage in this process"),
    "after_confirm": q("DOC021:T027", "I think like giving the information could be after confirming the availability from the 2 parties"),
    "not_before": q("DOC021:T027", "before that step I think it's not necessary to give all the information"),
    "two_ways": q("DOC021:T029", "I will have 2 ways either to fill the form inside the website"),
    "map_route": q("DOC021:T029", "or just to take their location from the map, then try to find more about them, using other websites like Google Map"),
    "draw_tool": q("DOC021:T033", "they provide sometimes a map with a drawing tool where you can just draw a circle around the place you're interested in in the map, and they will select the search inside that area"),
    "draw_flex": q("DOC021:T033", "by drawing. You can like, have more flexibility on selecting the area."),
    "reviews": q("DOC021:T033", "another thing that I like is providing reviews, I think reviews from people, makes. makes places feel more trusted"),
    "unknown_buttons": q("DOC021:T033", "multiple, unknown, like multiple buttons that you don't know. What would they proceed you to?"),
    "skip_site": q("DOC021:T033", "this type of long, unknown process makes me just skip the website"),
    "favorites_lost": q("DOC021:T035", "But actually, I can't find where where it's saving it."),
    "tour_form": q("DOC021:T035", "there is a button called Request a tour, and also it will have this form that you should fill"),
    "register_research": q("DOC021:T035", "when they require you to register just to do a research"),
    "compare_page": q("DOC021:T037", "sometimes I like 3 or 4 options like, I want to collect them all in in like a single page. So I can look in the main features at the same time."),
    "fav_weird": q("DOC021:T037", "the favorites button is. It's really weird because it might be saving it somewhere. But actually, I couldn't find it anywhere."),
    "nav_bar": q("DOC021:T039", "It should be like on the nav bar, or at least at the menu, at the like 1st level of the menu."),
    "optional_register": q("DOC021:T043", "It could be optional thing like if you want your information saved and to be filled directly you can register. But it should not be required."),
    "start_search": q("DOC021:T045", "Just start searching and seeing the whole functionality directly."),
    "no_steps": q("DOC021:T047", "to be more convenient just to search the information you want without having steps that you don't believe it's beneficial"),
    "filter_main": q("DOC021:T049", "You can filter by price range. you can filter by the number of beds and baths you can also filter by the home type whether you want a house, an apartment"),
    "filter_extra": q("DOC021:T049", "you can filter by extra criteria, like the move-in date, or any other things that you want, like allowing pets"),
    "filter_optional": q("DOC021:T051", "I like that. The filters are optional. They don't enforce you to enter everything"),
    "lose_options": q("DOC021:T051", "What if I filter by some criteria, and then I lost all the options where the owners didn't specify."),
    "include_unspecified": q("DOC021:T051", "maybe I would love if there is an option where I can have like. I can also allow the people who didn't specify, so I can see both"),
    "checkbox": q("DOC021:T053", "maybe if there is like a check box called include, for example, like the options that didn't determine"),
    "both_states": q("DOC021:T055", "The one who allowed and the one who didn't specify, and if I didn't click on the checkbox, I will have the ones who only specify that they allow."),
    "overview": q("DOC021:T057", "So I want to be able to know what are the options? And what are the price ranges, and so on."),
    "overview2": q("DOC021:T057", "will give me an overview about the price ranges about the available options"),
    "photo_rules": q("DOC021:T059", "maybe if the website has some sort of rules that enforces people who own these properties to take the picture in a specific format, for example, on, for example, sunlight using like specific angles"),
    "last_upd_wish": q("DOC021:T059", "another thing that I would really love is to have to be able to see when it was last updated"),
    "sufficient_except": q("DOC021:T067", "It's only the part where I said about like when it was last updated."),
    "up_to_date": q("DOC021:T069", "I just want to be assured that it's it's up to date."),
    "compare_wish": q("DOC021:T071", "I wish, if there is such feature that helps me to compare"),
    "clear_fast": q("DOC021:T071", "it will be very sufficient to communicate with the property owners through these websites. If the process was clear and fast."),
    "single_place": q("DOC021:T071", "It will be great to have all the housing communication in a single place."),
    "vague_button": q("DOC021:T071", "the process is not clear. You just have a vague button called. Send a message where you will fill a form and never know what will happen next."),
    "week_window": q("DOC021:T073", "sometimes you want to decide within a week or maximum a month"),
    "ui_insight": q("DOC021:T073", "changing something in in the ui to make the user have some insight about, how would the communication process be?"),
    "stay_inside": q("DOC021:T073", "This will make him like, trust the feature more, and never try something else, and just keep the communication in in the website."),
}
