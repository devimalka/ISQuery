doctally = '''
select a.doc_code,k.doc_name,count(b.doc_code),round(sum((b.price*b.qty)-(b.price*b.qty*b.disrate/100)),2) as value
from rms_doc_txnm a
inner join rms_doc_txnd b on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code and a.doc_code=b.doc_code and a.doc_no=b.doc_no
inner join rms_doc_codes k on a.sbu_code=k.sbu_code and a.doc_code=k.doc_code
where a.sbu_code='830' and a.loc_code='{loccode}' and a.mstat='VAL' and a.txn_date between '{sdate}' and '{edate} 23:59:59' group by a.doc_code
union
select c.doc_code,k.doc_name,count(c.doc_code),round(sum((d.rate*d.qty)-(d.rate*d.qty*d.disrate/100)),2) as value
from rms_grn_txnm c
inner join rms_grn_txnd d on c.sbu_code=d.sbu_code and c.loc_code=d.loc_code and c.doc_code=d.doc_code and c.doc_no=d.doc_no
inner join rms_doc_codes k on c.sbu_code=k.sbu_code and c.doc_code=k.doc_code
where c.sbu_code='830' and c.loc_code='{loccode}'
and DATE_FORMAT(c.txn_date,'%Y-%M-%D') between '{sdate}' and '{edate} 23:59:59' group by c.doc_code
union
select e.doc_code,k.doc_name,count(e.doc_code) ,sum(e.rec_amt) as value from rms_recm e
inner join rms_recd f on e.sbu_code=f.sbu_code and e.loc_code=f.loc_code and e.doc_code=f.doc_code and e.doc_no=f.doc_no
inner join rms_doc_codes k on e.sbu_code=k.sbu_code and e.doc_code=k.doc_code
where e.sbu_code='830' and e.loc_code='{loccode}' and e.mstat<>'CAN' and e.txn_date between '{sdate}' and '{edate} 23:59:59'
group by e.doc_code
'''














ntb25 = '''
select a.loc_code,c.promid,a.txn_date,a.mach_code,a.receiptno,a.user_id,c.seqno,d.supplier,a.plu_code,a.item_code,d.itm_desc,a.price,a.qty,(a.price*a.qty) Gross_value,a.disc_per,a.disc_amt as Total_discount,((a.price*a.qty/100)*12.5) as NTB_discount,
((a.price*a.qty/100)*12.5) as ARPICO_discount,b.cardbn,b.lasnum
FROM rms_pos_txn_det a
inner join rms_pospromotxn c
on a.sbu_code=c.sbucod and a.loc_code=c.loccod and a.txn_date=c.txndat and a.mach_code=c.maccod and a.user_id=c.userid and a.receiptno=c.recino and a.seq_no=c.seqno
inner join rms_itmmaster d
on a.sbu_code=d.sbu_code and a.loc_code=d.loc_code and a.plu_code=d.plu_code and a.item_code=d.item_code
left outer join rms_pos_pay_details b
on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code and a.txn_date=b.txn_date and a.mach_code=b.mach_code and a.user_id=b.user_id and a.receiptno=b.receiptno and b.pay_mode='cr'
where a.sbu_code='830' and a.inv_status='VALID' and a.loc_code = (select char_val from rms_sys_parameters where para_code='DEFLOC')
and a.txn_date in('2022-06-15') and c.promid in('2271')  and a.disc_per<>'0' and b.pay_mode='cr' and b.comp_code='17'
order by a.loc_code,a.txn_date,a.mach_code,a.receiptno,a.user_id,c.seqno'''




Sampath25FreshOffer = '''
select a.loc_code,c.promid,a.txn_date,a.mach_code,a.receiptno,a.user_id,c.seqno,d.supplier,a.plu_code,a.item_code,d.itm_desc,a.price,a.qty,(a.price*a.qty) Gross_value,a.disc_per,a.disc_amt as Total_discount,b.cardbn,b.lasnum
FROM rms_pos_txn_det a
inner join rms_pospromotxn c
on a.sbu_code=c.sbucod and a.loc_code=c.loccod and a.txn_date=c.txndat and a.mach_code=c.maccod and a.user_id=c.userid and a.receiptno=c.recino and a.seq_no=c.seqno
inner join rms_itmmaster d
on a.sbu_code=d.sbu_code and a.loc_code=d.loc_code and a.plu_code=d.plu_code and a.item_code=d.item_code
left outer join rms_pos_pay_details b
on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code and a.txn_date=b.txn_date and a.mach_code=b.mach_code and a.user_id=b.user_id and a.receiptno=b.receiptno and b.pay_mode='cr'
where a.sbu_code='830' and a.inv_status='VALID' and a.loc_code = (select char_val from rms_sys_parameters where para_code='DEFLOC')
and a.txn_date='2022-06-16' and c.promid in('2273')  and a.disc_per<>'0' and b.pay_mode='cr' and b.comp_code='09'
order by a.loc_code,a.txn_date,a.mach_code,a.receiptno,a.user_id,c.seqno
'''


peoples10billvalue = '''
select a.loc_code,l.loc_name as Location_Name,c.promid,a.txn_date,a.mach_code,a.receiptno,a.user_id,d.net_amt as Bill_NET_Amount,d.TOTAL_DIS as Total_Bill_discount,(d.net_amt+d.total_dis) as Bill_Gross_Value,(a.price*-1) as Peoples_Promo_Discount,
b.amount as Peoples_Card_Payment_Amount,b.cardbn,b.lasnum,b.voucherno,b.appcod,b.refnum,b.crdtyp,b.crdnam
FROM rms_pos_txn_det a
inner join rms_pospromotxn c
on a.sbu_code=c.sbucod and a.loc_code=c.loccod and a.txn_date=c.txndat and a.mach_code=c.maccod and a.user_id=c.userid and a.receiptno=c.recino and a.seq_no=c.seqno
inner join rms_pos_txn_mas d
on a.sbu_code=d.sbu_code and a.loc_code=d.loc_code and a.txn_date=d.txn_date and a.mach_code=d.mach_code and a.user_id=d.user_id and a.receiptno=d.receiptno
inner join rms_locations l
on d.sbu_code=l.sbu_code and d.loc_code=l.loc_code
left outer join rms_pos_pay_details b
on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code and a.txn_date=b.txn_date and a.mach_code=b.mach_code and a.user_id=b.user_id and a.receiptno=b.receiptno and b.pay_mode='cr'
where a.sbu_code='830' and a.inv_status='VALID' and d.inv_status='VALID' and a.loc_code = (select char_val from rms_sys_parameters where para_code='DEFLOC')
and a.txn_date='2022-06-17' and c.promid in('3143') and b.pay_mode='cr' and b.comp_code='04'
order by a.loc_code,c.txndat,c.maccod,a.receiptno,a.user_id
'''

Seylan_10_Debit_CARD = '''
select a.loc_code,l.loc_name as Location_Name,c.promid,a.txn_date,a.mach_code,a.receiptno,a.user_id,d.net_amt as Bill_NET_Amount,d.TOTAL_DIS as Total_Bill_discount,(d.net_amt+d.total_dis) as Bill_Gross_Value,(a.price*-1) as Seylan_Promo_Discount,
b.amount as Seylan_Card_Payment_Amount,b.cardbn,b.lasnum,b.voucherno,b.appcod,b.refnum,b.crdtyp,b.crdnam
FROM rms_pos_txn_det a
inner join rms_pospromotxn c
on a.sbu_code=c.sbucod and a.loc_code=c.loccod and a.txn_date=c.txndat and a.mach_code=c.maccod and a.user_id=c.userid and a.receiptno=c.recino and a.seq_no=c.seqno
inner join rms_pos_txn_mas d
on a.sbu_code=d.sbu_code and a.loc_code=d.loc_code and a.txn_date=d.txn_date and a.mach_code=d.mach_code and a.user_id=d.user_id and a.receiptno=d.receiptno
inner join rms_locations l
on d.sbu_code=l.sbu_code and d.loc_code=l.loc_code
left outer join rms_pos_pay_details b
on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code and a.txn_date=b.txn_date and a.mach_code=b.mach_code and a.user_id=b.user_id and a.receiptno=b.receiptno and b.pay_mode='cr'
where a.sbu_code='830' and a.inv_status='VALID' and d.inv_status='VALID' and a.loc_code = (select char_val from rms_sys_parameters where para_code='DEFLOC')
and a.txn_date='2022-06-17' and c.promid in('3144') and b.pay_mode='cr' and b.comp_code='03'
order by a.loc_code,c.txndat,c.maccod,a.receiptno,a.user_id
'''

combank10Billvalue = '''
select a.loc_code,l.loc_name as Location_Name,c.promid,a.txn_date,a.mach_code,a.receiptno,a.user_id,d.net_amt as Bill_NET_Amount,d.TOTAL_DIS as Total_Bill_discount,(d.net_amt+d.total_dis) as Bill_Gross_Value,(a.price*-1) as COMM_Promo_Discount,
b.amount as COMM_Card_Payment_Amount,b.cardbn,b.lasnum,b.voucherno,b.appcod,b.refnum,b.crdtyp,b.crdnam
FROM rms_pos_txn_det a
inner join rms_pospromotxn c
on a.sbu_code=c.sbucod and a.loc_code=c.loccod and a.txn_date=c.txndat and a.mach_code=c.maccod and a.user_id=c.userid and a.receiptno=c.recino and a.seq_no=c.seqno
inner join rms_pos_txn_mas d
on a.sbu_code=d.sbu_code and a.loc_code=d.loc_code and a.txn_date=d.txn_date and a.mach_code=d.mach_code and a.user_id=d.user_id and a.receiptno=d.receiptno
inner join rms_locations l
on d.sbu_code=l.sbu_code and d.loc_code=l.loc_code
left outer join rms_pos_pay_details b
on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code and a.txn_date=b.txn_date and a.mach_code=b.mach_code and a.user_id=b.user_id and a.receiptno=b.receiptno and b.pay_mode='cr'
where a.sbu_code='830' and a.inv_status='VALID' and d.inv_status='VALID' and a.loc_code = (select char_val from rms_sys_parameters where para_code='DEFLOC')
and a.txn_date='2022-06-18' and c.promid in('3142') and b.pay_mode='cr' and b.comp_code='10'
order by a.loc_code,c.txndat,c.maccod,a.receiptno,a.user_id
'''


seylan10BillVAlue = '''
select a.loc_code,l.loc_name as Location_Name,c.promid,a.txn_date,a.mach_code,a.receiptno,a.user_id,d.net_amt as Bill_NET_Amount,d.TOTAL_DIS as Total_Bill_discount,(d.net_amt+d.total_dis) as Bill_Gross_Value,(a.price*-1) as Seylan_Promo_Discount,
b.amount as Seylan_Card_Payment_Amount,b.cardbn,b.lasnum,b.voucherno,b.appcod,b.refnum,b.crdtyp,b.crdnam
FROM rms_pos_txn_det a
inner join rms_pospromotxn c
on a.sbu_code=c.sbucod and a.loc_code=c.loccod and a.txn_date=c.txndat and a.mach_code=c.maccod and a.user_id=c.userid and a.receiptno=c.recino and a.seq_no=c.seqno
inner join rms_pos_txn_mas d
on a.sbu_code=d.sbu_code and a.loc_code=d.loc_code and a.txn_date=d.txn_date and a.mach_code=d.mach_code and a.user_id=d.user_id and a.receiptno=d.receiptno
inner join rms_locations l
on d.sbu_code=l.sbu_code and d.loc_code=l.loc_code
left outer join rms_pos_pay_details b
on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code and a.txn_date=b.txn_date and a.mach_code=b.mach_code and a.user_id=b.user_id and a.receiptno=b.receiptno and b.pay_mode='cr'
where a.sbu_code='830' and a.inv_status='VALID' and d.inv_status='VALID' and a.loc_code = (select char_val from rms_sys_parameters where para_code='DEFLOC')
and a.txn_date='2022-06-18' and c.promid in('3141') and b.pay_mode='cr' and b.comp_code='03'
order by a.loc_code,c.txndat,c.maccod,a.receiptno,a.user_id'''


bocTopUP = '''
select a.loc_code,c.promid,a.txn_date,a.mach_code,a.receiptno,a.user_id,c.seqno,d.supplier,a.plu_code,a.item_code,d.itm_desc,a.price,a.qty,(a.price*a.qty) Gross_value,a.disc_per,a.disc_amt as Total_discount,
(((a.price*a.qty)/100)*15) as BOC_TopUp_Promo_discount,(a.disc_amt-(((a.price*a.qty)/100)*15)) as ARPICO_discount,b.cardbn,b.lasnum
FROM rms_pos_txn_det a
inner join rms_pospromotxn c
on a.sbu_code=c.sbucod and a.loc_code=c.loccod and a.txn_date=c.txndat and a.mach_code=c.maccod and a.user_id=c.userid and a.receiptno=c.recino and a.seq_no=c.seqno
inner join rms_itmmaster d
on a.sbu_code=d.sbu_code and a.loc_code=d.loc_code and a.plu_code=d.plu_code and a.item_code=d.item_code
left outer join rms_pos_pay_details b
on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code and a.txn_date=b.txn_date and a.mach_code=b.mach_code and a.user_id=b.user_id and a.receiptno=b.receiptno and b.pay_mode='cr'
where a.sbu_code='830' and a.inv_status='VALID' and a.loc_code = (select char_val from rms_sys_parameters where para_code='DEFLOC')
and a.txn_date between '2022-06-04' and '2022-06-18' and c.promid in('2256','2258','2267','2276')  and a.disc_per<>'0' and b.pay_mode='cr' and b.comp_code='19'
order by a.loc_code,a.txn_date,a.mach_code,a.receiptno,a.user_id,c.seqno'''