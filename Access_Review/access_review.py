import os

f = open('HashicorpVault_Access_Review.csv', 'w')
f.write("UserID,CreateTime,Login_Type,Namespace,Group\n")
ns = os.popen('''vault namespace list | egrep -v 'Keys|----' ''').read().strip()

for n in ns.split('\n'):
	get_entities = ''
	get_entities = os.popen('''vault list -namespace=%s identity/entity/id | egrep -v 'Keys|----' ''' %n).read().strip()
	if get_entities == '':
		print("No user entities under Namespace: %s\n" %n)
		f.write("No user entities under Namespace: %s\n" %n)
	else:
		for e in get_entities.split('\n'):
			user_det = ''
			g_id = ''
			name = ''
			ctime = ''
			type1 = ''
			group = ''
			user_det = os.popen('''vault read -namespace=%s -format=json identity/entity/id/%s | jq -r ".data.aliases" | egrep -w 'creation_time|name|mount_type' ''' %(n,e) ).read().strip()
			if user_det != '':
				g_id = os.popen('''vault read -namespace=%s -format=json identity/entity/id/%s | jq -r ".data.direct_group_ids" | grep '"' ''' %(n,e)).read().strip()
				for u in user_det.split('\n'):
					if "name" in u:
						name = u.split(": ")[1].split('"')[1].split('"')[0]
					if "creation_time" in u:
						ctime = u.split(": ")[1].split('"')[1].split('"')[0]
					if "mount_type" in u:
						type1 = u.split(": ")[1].split('"')[1].split('"')[0]
				if len(g_id.split('\n')) == 1:
					if type1 == "ldap":
						group = os.popen('''vault read -namespace=%s -format=json identity/group/id/%s | jq -r ".data.name" ''' %(n,g_id)).read().strip()
					else:
						group = ''
					print("%s,%s,%s,%s,%s" %(name,ctime,type1,n,group))
					f.write("%s,%s,%s,%s,%s\n" %(name,ctime,type1,n,group))
				else:
					for g in g_id.split('\n'):
						if type1 == "ldap":
							group = os.popen('''vault read -namespace=%s -format=json identity/group/id/%s | jq -r ".data.name" ''' %(n,g.strip().split(',')[0])).read().strip()
						else:
							group = ''
						print("%s,%s,%s,%s,%s" %(name,ctime,type1,n,group))
						f.write("%s,%s,%s,%s,%s\n" %(name,ctime,type1,n,group))
			else:
				print("No Aliases for entity_id: %s under Namespace: %s" %(e, n))
				f.write("No Aliases for entity_id: %s under Namespace: %s\n" %(e, n))
				
f.close()