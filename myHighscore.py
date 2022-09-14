class hs_record:
    def __init__(self,name,score,position = 0):
        self.name = name
        self.score = score
        self.position = position

    def isWorking(self):
        return True


def sortRecords(records):
    #Sorts a list 'records' containing objects of type 'hs_record'
    sorted_records = []
    for record in records:
        placed =  False
        if sorted_records == []:
            sorted_records.append(record)
        else:
            for j,srecord in enumerate(sorted_records):
                
                if placed:
                    break
                if record.score > srecord.score:
                    sorted_records.insert(j,record)
                    placed = True
            if not placed:      
                #then record score is lowest
                sorted_records.append(record)
    for i,record in enumerate(sorted_records):
        record.position = i+1
    return sorted_records
                    



if __name__=='__main__':
    record1 = hs_record(1,'ayush',840)
    record2 = hs_record(2,'ayu',940)
    record3 = hs_record(4,'ayus',700)
    record4 = hs_record(4,'ayushh',1500)
    record5 = hs_record(4,'a',750)
    hsrecords = [record1,record2,record3,record4,record5]
    hsrecords = sortRecords(hsrecords)
    print([(r.position,r.name,r.score) for r in hsrecords])

    
