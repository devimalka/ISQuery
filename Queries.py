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



psal = '''
select a.loc_code,c.promid,a.txn_date,a.mach_code,a.receiptno,c.seqno,a.plu_code,a.item_code,d.itm_desc,a.qty,a.price,(a.price*a.qty) as Gross_value,'12.5%',((a.price*a.qty/100)*12.5) as SCB_discount,'12.5%',((a.price*a.qty/100)*12.5) as ARPICO_discount, a.disc_amt as Total_discount,
b.amount as paid_amount_by_card,b.cardbn,b.lasnum
FROM rms_pos_txn_det a
inner join rms_pospromotxn c
on a.sbu_code=c.sbucod and a.loc_code=c.loccod and a.txn_date=c.txndat and a.mach_code=c.maccod and a.user_id=c.userid and a.receiptno=c.recino and a.seq_no=c.seqno
inner join rms_itmmaster d
on a.sbu_code=d.sbu_code and a.loc_code=d.loc_code and a.plu_code=d.plu_code and a.item_code=d.item_code
left outer join rms_pos_pay_details b
on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code and a.txn_date=b.txn_date and a.mach_code=b.mach_code and a.user_id=b.user_id and a.receiptno=b.receiptno and b.pay_mode='cr'
where a.sbu_code='830' and a.inv_status='VALID' and a.loc_code = (select char_val from rms_sys_parameters where para_code='DEFLOC')
and a.txn_date between '2022-03-11' and '2022-03-13' and c.promid in('2172') and a.disc_per<>'0' and b.comp_code='02' and b.pay_mode='cr'
order by a.txn_date,a.receiptno,a.mach_code,a.seq_no


'''



hnb = '''
select a.loc_code,c.promid,a.txn_date,a.mach_code,a.receiptno,a.user_id,c.seqno,d.supplier,a.plu_code,a.item_code,d.itm_desc,a.price,a.qty,(a.price*a.qty) Gross_value,a.disc_per,a.disc_amt as Total_discount,((a.price*a.qty/100)*12.5) as HNB_discount,
((a.price*a.qty/100)*12.5) as ARPICO_discount,b.cardbn,b.lasnum
FROM rms_pos_txn_det a
inner join rms_pospromotxn c
on a.sbu_code=c.sbucod and a.loc_code=c.loccod and a.txn_date=c.txndat and a.mach_code=c.maccod and a.user_id=c.userid and a.receiptno=c.recino and a.seq_no=c.seqno
inner join rms_itmmaster d
on a.sbu_code=d.sbu_code and a.loc_code=d.loc_code and a.plu_code=d.plu_code and a.item_code=d.item_code
left outer join rms_pos_pay_details b
on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code and a.txn_date=b.txn_date and a.mach_code=b.mach_code and a.user_id=b.user_id and a.receiptno=b.receiptno and b.pay_mode='cr'
where a.sbu_code='830' and a.inv_status='VALID' and a.loc_code = (select char_val from rms_sys_parameters where para_code='DEFLOC')
and a.txn_date in('2022-04-16','2022-04-17') and c.promid in('2201')  and a.disc_per<>'0' and b.pay_mode='cr' and b.comp_code='08'
order by a.loc_code,a.txn_date,a.mach_code,a.receiptno,a.user_id,c.seqno'''




union = '''select a.loc_code,l.loc_name as Location_Name,c.promid,a.txn_date,a.mach_code,a.receiptno,a.user_id,d.net_amt as Bill_NET_Amount,d.TOTAL_DIS as Total_Bill_discount,(d.net_amt+d.total_dis) as Bill_Gross_Value,(a.price*-1) as UNION_Promo_Discount,
b.amount as UNION_Card_Payment_Amount,b.cardbn,b.lasnum,b.voucherno,b.appcod,b.refnum,b.crdtyp,b.crdnam
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
and a.txn_date='2022-04-14' and c.promid in('3087') and b.pay_mode='cr' and b.comp_code='25'
order by a.loc_code,c.txndat,c.maccod,a.receiptno,a.user_id'''


SCB='''
select a.loc_code,c.promid,a.txn_date,a.mach_code,a.receiptno,c.seqno,a.plu_code,a.item_code,d.itm_desc,a.qty,a.price,(a.price*a.qty) as Gross_value,'12.5%',((a.price*a.qty/100)*12.5) as SCB_discount,'12.5%',((a.price*a.qty/100)*12.5) as ARPICO_discount, a.disc_amt as Total_discount,
b.amount as paid_amount_by_card,b.cardbn,b.lasnum
FROM rms_pos_txn_det a
inner join rms_pospromotxn c
on a.sbu_code=c.sbucod and a.loc_code=c.loccod and a.txn_date=c.txndat and a.mach_code=c.maccod and a.user_id=c.userid and a.receiptno=c.recino and a.seq_no=c.seqno
inner join rms_itmmaster d
on a.sbu_code=d.sbu_code and a.loc_code=d.loc_code and a.plu_code=d.plu_code and a.item_code=d.item_code
left outer join rms_pos_pay_details b
on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code and a.txn_date=b.txn_date and a.mach_code=b.mach_code and a.user_id=b.user_id and a.receiptno=b.receiptno and b.pay_mode='cr'
where a.sbu_code='830' and a.inv_status='VALID' and a.loc_code = (select char_val from rms_sys_parameters where para_code='DEFLOC')
and a.txn_date between '2022-04-15' and '2022-04-17' and c.promid in('2203') and a.disc_per<>'0' and b.comp_code='02' and b.pay_mode='cr'
order by a.txn_date,a.receiptno,a.mach_code,a.seq_no'''



sithumina = '''
SELECT a.loc_code,a.item_code,b.plu_code,b.itm_desc,a.itmfac,a.gonstk FROM marksys.rms_stockloc_inv a
left outer join marksys.rms_itmmaster b on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code
and a.item_code=b.item_code
where a.sbu_code='830' and a.stock_loc='00' and itmfac<>'0'  and gonstk<>'0'
group by a.loc_code,a.item_code,b.itm_desc;'''



ddd='''
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
and a.txn_date='2022-05-13' and c.promid in('3111') and b.pay_mode='cr' and b.comp_code='03'
order by a.loc_code,c.txndat,c.maccod,a.receiptno,a.user_id'''


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
and a.txn_date in('2022-06-08') and c.promid in('2262')  and a.disc_per<>'0' and b.pay_mode='cr' and b.comp_code='17'
order by a.loc_code,a.txn_date,a.mach_code,a.receiptno,a.user_id,c.seqno'''


peoples10billvalue ='''
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
and a.txn_date='2022-06-03' and c.promid in('3134') and b.pay_mode='cr' and b.comp_code='04'
order by a.loc_code,c.txndat,c.maccod,a.receiptno,a.user_id'''


dfcc10 = '''
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
and a.txn_date='2022-06-11' and c.promid in('3131') and b.pay_mode='cr' and b.comp_code='20'
order by a.loc_code,c.txndat,c.maccod,a.receiptno,a.user_id'''


scbcopy = '''
select a.loc_code,c.promid,a.txn_date,a.mach_code,a.receiptno,c.seqno,a.plu_code,a.item_code,d.itm_desc,a.qty,a.price,(a.price*a.qty) as Gross_value,'12.5%',((a.price*a.qty/100)*12.5) as SCB_discount,'12.5%',((a.price*a.qty/100)*12.5) as ARPICO_discount, a.disc_amt as Total_discount,
b.amount as paid_amount_by_card,b.cardbn,b.lasnum
FROM rms_pos_txn_det a
inner join rms_pospromotxn c
on a.sbu_code=c.sbucod and a.loc_code=c.loccod and a.txn_date=c.txndat and a.mach_code=c.maccod and a.user_id=c.userid and a.receiptno=c.recino and a.seq_no=c.seqno
inner join rms_itmmaster d
on a.sbu_code=d.sbu_code and a.loc_code=d.loc_code and a.plu_code=d.plu_code and a.item_code=d.item_code
left outer join rms_pos_pay_details b
on a.sbu_code=b.sbu_code and a.loc_code=b.loc_code and a.txn_date=b.txn_date and a.mach_code=b.mach_code and a.user_id=b.user_id and a.receiptno=b.receiptno and b.pay_mode='cr'
where a.sbu_code='830' and a.inv_status='VALID' and a.loc_code = (select char_val from rms_sys_parameters where para_code='DEFLOC')
and a.txn_date between '2022-06-04' and '2022-06-12' and c.promid in('2255','2265') and a.disc_per<>'0' and b.comp_code='02' and b.pay_mode='cr'
order by a.txn_date,a.receiptno,a.mach_code,a.seq_no
'''