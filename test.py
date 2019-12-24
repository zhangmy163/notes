import random
import itertools

#维度对应的数据源
dms={
    "placement,placement_id":["union_datasource"],
    "ad_goal":["union_datasource"],
    "ad_car_model_name":["union_datasource"],
    "impression_monitoring":["union_datasource"],
    "click_monitoring":["union_datasource"],
    "ad_creativity":["union_datasource"],
    "ad_size":["union_datasource"],
    "ad_section":["union_datasource"],
    "purchase_unit":["union_datasource"],
    "activity_monitoring":["union_datasource"],
    "ad_form_loc":["union_datasource"],
    "city_level":["union_datasource"],
    "user_age_bracket":["user_age_distdc"],
    "user_gender_name":["user_gender_distdc"],
    "province":["user_region_distdc"],
    "interest_category_name":["interest_category_distdc"],
    "device_category":["union_datasource","device_category_distdc"],
    "city":["union_datasource","user_region_distdc"],
    "advertiser,advertiser_id":["device_category_distdc","interest_category_distdc","union_datasource","user_age_distdc","user_gender_distdc","user_region_distdc"],
    "site_imedia":["device_category_distdc","interest_category_distdc","union_datasource","user_age_distdc","user_gender_distdc","user_region_distdc"],
    "site_category,site_ca_id":["device_category_distdc","interest_category_distdc","union_datasource","user_age_distdc","user_gender_distdc","user_region_distdc"],
    "campaign,campaign_id":["device_category_distdc","interest_category_distdc","union_datasource","user_age_distdc","user_gender_distdc","user_region_distdc"],
    "day":["device_category_distdc","interest_category_distdc","union_datasource","user_age_distdc","user_gender_distdc","user_region_distdc"],
    "month":["device_category_distdc","interest_category_distdc","union_datasource","user_age_distdc","user_gender_distdc","user_region_distdc"],
    "site,site_id":["device_category_distdc","interest_category_distdc","union_datasource","user_age_distdc","user_gender_distdc","user_region_distdc","overlap"]
}
#数据源对应的指标
mes={
    "union_datasource":["sum__imp_count","sum__estimated_impression","imp_target_rate","sum__click_count","sum__estimated_click","click_target_rate","click_rate","sum__net_price","actual_cpm","actual_cpc","sum__imp_valid_traffic","total_imp_count","valid_imp_rate","sum_dcm_invalid_imp_count","sum_cig_invalid_imp_count","dcm_invalid_imp_percent","cig_invalid_imp_percent","ecpm","sum__click_valid_traffic","total_click_count","valid_click_rate","sum_dcm_invalid_click_count","sum_cig_invalid_click_count","dcm_invalid_click_percent","cig_invalid_click_percent","ecpc","total_valid_coverage","total_valid_coverage_rate","cig_invalid_coverage_rate","sum__ga_valid_traffic","valid_arrival_rate","cig_invalid_arrival_rate","ecpv","ecpl","count_distinct__imp_user","count_distinct__click_user","total_coverage","count_distinct__ga_user","count_distinct__submit_clue_user","average_imp_frequency","average_click_frequency","unique_cpm","unique_cpc","unique_landing_cost","unique_cpl","media_coverage","count_distinct__clue","arrival_rate","new_session_rate","cpl","count_distinct__ga_user","sum__pageviews","count_distinct__ga_user","sum__clue_count","sum__session_count","bounce_rate","average_time_on_site","average_pageviews","conversion_ratio","sum__scount"],
    "overlap":["unique_total_coverage","overlap_total_coverage","media_overlap_rate_p","media_overlap_rate","unique_imp_coverage","overlap_imp_coverage","imp_overlap_rate_p","imp_overlap_rate","unique_click_coverage","overlap_click_coverage","click_overlap_rate_p","click_overlap_rate","unique_ga_coverage","overlap_ga_coverage","ga_overlap_rate_p","ga_overlap_rate","unique_clue","overlap_clue","clue_overlap_rate_p","clue_overlap_rate"],
    "user_age_distdc":["sum__user_count","sum__pageviews","sum__user_count","sum__leads_count","sum__session_count","bounce_rate","average_time_on_site","average_pageviews","conversion_ratio","sum__scount","sum__new_user_count"],
    "user_gender_distdc":["sum__user_count","sum__pageviews","sum__user_count","sum__leads_count","sum__session_count","bounce_rate","average_time_on_site","average_pageviews","conversion_ratio","sum__scount","sum__new_user_count"],
    "user_region_distdc":["sum__user_count","sum__pageviews","sum__user_count","sum__leads_count","sum__session_count","bounce_rate","average_time_on_site","average_pageviews","conversion_ratio","sum__scount","sum__new_user_count"],
    "interest_category_distdc":["sum__user_count","sum__pageviews","sum__user_count","sum__leads_count","sum__session_count","bounce_rate","average_time_on_site","average_pageviews","conversion_ratio","sum__scount","sum__new_user_count"],
    "device_category_distdc":["sum__user_count","sum__pageviews","sum__user_count","sum__leads_count","sum__session_count","bounce_rate","average_time_on_site","average_pageviews","conversion_ratio","sum__scount","sum__new_user_count"]
}
# print(dms["A"])
# print(dms.keys())
# print(dms.values())

#随机取维度
#random dms
# dm=random.sample(dms.keys(),2)

#排列组合维度，(a,b),(b,c)，
dm=itertools.combinations(dms.keys(),3)
#初始化存放数据源的list
lastds=[]
#循环维度的排列组合
for i in list(dm):
    # print(i)
    for j in i:
        # print(j)
        # 取维度的数据源合并到一个list,lastds
        lastds.append(dms[j])
    # 根据lastds的数据源取交集
    ins_tmp=set(lastds[0]).intersection(*lastds[1:])
    ins=list(ins_tmp)
    # 判断交集len，0无交集，1有一个交集数据源，>1有多个交集数据源
    # 当无交集时，循环维度，从维度数据源中随机1个，在该数据源中随机3个指标，然后把维度，数据源:指标拼起来
    if(len(ins)==0):
        mestmp=[]
        for d in i:
            ds=random.sample(dms[d],1)[0]
            me=",".join(["%s:%s" %(ds,m) for m in random.sample(mes[ds],3)])
            mestmp.append(me)
        # print(i)
        lastdms=",".join(i)
        lastmes=",".join(mestmp)
        print(lastdms+","+lastmes)        
    # 当有1个交集时，把该数据源下的所有指标拼接数据源，然后维度，数据源:指标返回    
    elif(len(ins)==1):
        lastdms=",".join(i)
        lastmes=",".join(["%s:%s"%(ins[0],m) for m in mes[ins[0]]])
        print(lastdms+","+lastmes)
    # 当多余一个交集时，从交集的数据源随机两个，然后每个数据源随机3个指标，拼接维度，数据源:指标
    elif(len(ins)>1):
        dsrandom=random.sample(ins,2)
        mestmp=[]
        for d in dsrandom:
            me=",".join(["%s:%s" %(d,m) for m in random.sample(mes[d],3)])
            mestmp.append(me)
        lastdms=",".join(i)
        lastmes=",".join(mestmp)
        print(lastdms+","+lastmes)

    lastds=[]
