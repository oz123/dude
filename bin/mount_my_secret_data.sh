#echo "Enter your password"
#read -s password
#echo "passphrase_passwd=$password" > foo
#mount -t ecryptfs -o ecryptfs_fnek_sig=a0a4fcf7e16b5778,ecryptfs_passthrough=no,ecryptfs_cipher=aes,ecryptfs_key_bytes=32,ecryptfs_enable_filename_crypto=yes,key=passphrase:passphrase_passwd_file=/home/oznt/foo /home/data/ /home/data/
#rm foo

mount -t ecryptfs -o ecryptfs_passthrough=no,ecryptfs_cipher=aes,ecryptfs_key_bytes=32,ecryptfs_enable_filename_crypto=yes /home/Data/ /home/Data/

