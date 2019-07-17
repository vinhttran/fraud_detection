import numpy as np
import pandas as pd

def ticket_types(df):
    new_df=pd.DataFrame(df.ticket_types[0])
    result_df=new_df[['quantity_sold', 'quantity_total', 'event_id']].groupby('event_id').sum()
    result_df=result_df.join(new_df[['availability', 'cost', 'event_id']].groupby('event_id').mean())

    for i in range(1,df.shape[0]):
        try:
            df_element=pd.DataFrame(df.ticket_types[i])
            grp_ele_df=df_element[['quantity_sold', 'quantity_total', 'event_id']].groupby('event_id').sum()
            grp_ele_df=grp_ele_df.join(df_element[['availability', 'cost', 'event_id']].groupby('event_id').mean())
            result_df=pd.concat([result_df, grp_ele_df])

        except:
            continue
    result_df.reset_index(inplace=True)
    result_df.columns=['object_id', 'quantity_sold', 'quantity_total', 'availability', 'cost']
    final_df=df.set_index('object_id').join(result_df.set_index('object_id'))
    final_df.reset_index(inplace=True)
    final_df[['quantity_sold', 'quantity_total','availability', 'cost']]=final_df[['quantity_sold', 'quantity_total','availability', 'cost']].fillna(0)
    return final_df

def prev_pay_count(df):
    df.previous_payouts=df.previous_payouts.apply(lambda x: len(x))
    return df

def clean_rest(df):
    df.venue_country=df.venue_country.isna()
    df.name_length=df.name_length==0
    df=pd.get_dummies(df,columns = ['payout_type','listed'])
    df=df[['body_length', 'channels', 'country', 'delivery_method', 'email_domain', 
       'fb_published', 'gts', 'has_analytics', 'has_header', 'has_logo',
        'name_length', 'num_order', 'num_payouts', 'org_desc','org_facebook',
       'org_name', 'org_twitter', 'payee_name','previous_payouts', 'show_map',
        'user_age', 'user_type',
       'venue_address', 'venue_country','quantity_sold', 'quantity_total',
       'availability', 'cost', 'fraud', 'payout_type_', 'payout_type_ACH',
       'payout_type_CHECK', 'listed_n', 'listed_y']]
    df=df.fillna(0)*1
    
    return df

def isexist(df, col):
    df[col]=df[col].apply(lambda x: len(x))==0
    return df

def country_classify(df, col='country'):
    country_filter=['JM', 'BG', 'ID', 'NG', 'PK', 'VN', 'GH', 'TR', 'SI', 'RU', 'A1', 'CH',
       'CI', 'CM', 'PS', 'JE', 'CN', 'PH', 'CZ', 'DK', 'DZ', 'NA', 'MY', 'MA',
       'KH', 'CO', 'IL']
    df[col]=df[col].apply(lambda x : x in country_filter)
    df[col].astype('int64')
    return df

def email_classify(df, col='email_domain'):
    email_filter=['outlook.com', 'mail.com', 'ymail.com', 'techie.com', 'inbox.com',
       'gmx.com', 'hotmail.fr', 'yahoo.fr', 'rocketmail.com',
       'mohmal.com', 'noiphuongxa.com', 'live.FR', 'nbuux.com',
       'naworld-x.com', 'myway.com', 'live.fr', 'medicalrepinsight.com',
       'lmtexformula.com', 'london.com', 'lushsaturdays.co.uk',
       'maroclancers.com', 'monkeyadvert.com', 'live.de', '126.com',
       'post.com', 'outlook.fr', 'yahoo.it', 'yahoo.de', 'yahoo.com.vn',
       'yahoo.co.id', 'vncall.net', 'visichathosting.net', 'usa.com',
       'ultimatewine.co.uk', 'twcny.rr.com', 'toke.com',
       'thinktankconsultancy.com', 'student.framingham.edu',
       'startupmaroc.com', 'socialworker.net', 'safe-mail.net',
       'rock.com', 'ravemail.com', 'quaychicago.com',
       'qualityservice.com', 'qip.ru', 'primehire.co.uk', 'lidf.co.uk',
       'photographer.net', 'petlover.com', 'ovidcapita.com', 'outlook.de',
       'levyresourcesinc.com', 'investocorp.com', 'keromail.com',
       'cyberservices.com', 'contractor.net', 'consultant.com',
       'clothmode.com', 'clerk.com', 'chef.net', 'checker.vn',
       'cdrenterprise.net', 'catchatt.com', 'cannapro.com',
       'brew-meister.com', 'brew-master.com', 'discofan.com',
       'blader.com', 'aol.co.uk', 'angelwish.org', 'anasconcept.com',
       'accountant.com', 'The2Half.com', 'Safe-mail.net',
       'DionJordan.com', '9and1.biz', '4u2nv-ent.com', '4asdkids.com',
       '31and7.com', '19sieunhan.com', 'ashfordradtech.org',
       'diversity-church.com', 'dr.com', 'emgay.com', 'kbzaverigroup.com',
       'jobsfc.com', 'jcclain.com', 'izzane.net', 'ioccupied.net',
       'yopmail.com', 'insuranceadjustersinc.com', 'instructor.net',
       'inorbit.com', 'innovateyours.com', 'indiabestplace.com',
       'indglobal-consulting.com', 'in.com', 'hushmail.com', 'hotmail.de',
       'hotelvenizbaguio.com', 'hmshost.com', 'hamptonmedi.com',
       'greenrcs.com', 'gosimplysocial.com', 'gcase.org', 'gawab.com',
       'fridayzonmarz.co.uk', 'freya.pw', 'execs.com', 'europe.com',
       'eng.uk.com', 'leisurelodgebaguio.com', 'zumba-perth.com']
    df[col]=df[col].apply(lambda x : x in email_filter)
    df[col].astype('int64')
    return df

def create_target(df):
    df['fraud'] = df['acct_type'].map({'fraudster_event': 1,
                                   'premium': 0,
                                   'spammer_warn': 0,
                                   'fraudster': 1,
                                   'spammer_limited': 0,
                                   'spammer_noinvite': 0,
                                   'locked': 0,  #changed to 0 from 1
                                   'tos_lock': 0,
                                   'tos_warn': 0,
                                   'fraudster_att': 1,
                                   'spammer_web': 0,
                                   'spammer': 0})
    return df

def pre_process_data(df):
    df=ticket_types(df)
    df=create_target(df)
    df=prev_pay_count(df)
    df=email_classify(df)
    df=country_classify(df)
    df=isexist(df,'org_name')
    df=isexist(df,'payee_name')
    df=isexist(df,'venue_address')
    df=isexist(df,'org_desc')
    df=clean_rest(df)
    return df
