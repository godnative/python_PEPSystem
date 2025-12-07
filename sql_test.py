from DataBase.holyevent_db import HolyEventDB

if __name__ == '__main__':
    with HolyEventDB(None) as db:
        exd = {'holyevent_p1_id': 1,
               'holyevent_p2_id': 1,
               'holyevent_implementer': '123',
               'holyevent_witness': '456',
               'holyevent_school_id': 1,
               'holyevent_date': 1750550400,
               'operator': 'admin',
               'opera_time': 1750586967,
               'opera_type': None,
               'holyevent_note': '123',
               'holyevent_id': 1}

        print(db.fetch_all_event_by_type(1, 1))