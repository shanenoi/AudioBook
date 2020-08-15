cat tts_temp_*.mp3 > $1.meom &&
rm tts_temp_*.mp3 &&
mv $1.meom $1.mp3
