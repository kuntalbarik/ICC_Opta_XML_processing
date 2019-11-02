# ICC_Opta_XML_processing
1)C2 and C3 will be generated using match no
2)First C2 ,then C3 will be processed.
3)If C2 is dropped in inbox and not processed in 7 minutes, execution will stop
4)Once C2 is processed successfully (file is in success folder),then only c3 will be dropped in inbox.
5)Once C3 is processed successfully (file is in success folder),then only c50 will be cut+paste/copy+paste from
   c50 source location and will be renamed.
6)NOTE--for point 4 and 5 if c2 and c3 is in unhandled failure or in any other location except success folder, execution will stop.
7)Once c50 are renamed, all c50 will be dropped in inbox folder.
