

##### Change this to your directories
ROOT=/mount/arbeitsdaten40/projekte/asr/wiengale
ESPNET=${ROOT}/espnet
ALIGNER=${ROOT}/Aligner
PROSCRIPTER=${ROOT}/Proscripter-master
PUNKPROSE=${ROOT}/punkProse-master
MODELNAME=Model_single-stage_wPOSpausf0m.pcl
INPUT=/mount/arbeitsdaten40/projekte/asr/wiengale/espnet/egs/an4/asr1/downloads/newdatadata

stage=0

# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

############# Need two run-files: with and without scoring

if [ ${stage} -le 0 ]; then
	###### Decode with espnet
	echo "Stage 0: Prepare data for espnet"
	mkdir /mount/arbeitsdaten40/projekte/asr/wiengale/espnet/egs/an4/asr1/data/newdatadata
	python src/data_prep.py --d ${INPUT}

fi


if [ ${stage} -le 1 ]; then
	###### Decode with espnet
	echo "Stage 1: Decoding with espnet"
	cd ${ESPNET}/egs/an4/asr1/
	./myrun.sh --backend chainer

fi


if [ ${stage} -le 2 ]; then
	###### Prepare data for IMS Aligner
	echo "Stage 2: Forced Alignment"
	cd ${ROOT}/src
	# somehow copy wav files into Aligner dir
	for filename in ../espnet/egs/an4/asr1/downloads/newdatadata/wav/*.sph; do 
		/mount/arbeitsdaten40/projekte/asr/wiengale/espnet/egs/an4/asr1/../../../tools/kaldi/tools/sph2pipe_v2.5/sph2pipe -f wav -p -c 1 $filename $filename.wav;
		mv $filename.wav ${ALIGNER}
	done
	# create Aligner input from espnet output (dynamischer Link?)
	python esp2Aligner.py --o ${ALIGNER} --d ${ESPNET}/egs/an4/asr1/exp/train_nodev_blstmp_e4_subsample1_2_2_1_1_unit320_proj320_d1_unit300_location_aconvc10_aconvf100_mtlalpha0.5_adadelta_bs30_mli800_mlo150/decode_newdatadata

	###### Align with IMS Aligner
	cd ${ALIGNER}
	for filename in ${ALIGNER}/*.wav; do
		Alignwords ${filename};
	done

fi


if [ ${stage} -le 3 ]; then
	###### Prepare data for Proscripter
	echo "Stage 3: Preparation for punctuation annotation with Proscripter"
	cd ${ROOT}/src
	for filename in ${ALIGNER}/*.words; do
		python IMS2Proscripter.py --f "${filename}";
	done

	###### Proscript
	cd ${PROSCRIPTER}
	mkdir out_predictions
	./run.sh ${ALIGNER}/${INPUT} ${ALIGNER}/"${INPUT/.wav/.align}" out_predictions

fi


if [ ${stage} -le 4 ]; then
	###### Prepare data for punkProse
	echo "Stage 4: Punctuation annotation with punkProse"
	cd ${PUNKPROSE}
	mkdir corpus; cd corpus
	mkdir dev_samples; mkdir test_samples; mkdir train_samples; mkdir test_groundtruth
	cd ${ROOT}/src
	python Proscripter2punkProse.py --f ${PROSCRIPTER}/out_predictions/"${INPUT/.wav/}"/proscript/"${INPUT/.wav/.proscript.csv}"
	mv -f vocabulary.txt ${PUNKPROSE}/corpus; mv -f pos_vocabulary.txt ${PUNKPROSE}/corpus
	mv ${PROSCRIPTER}/out_predictions/"${INPUT/.wav/}"/proscript/"${INPUT/.wav/.csv}" ${PUNKPROSE}/corpus/test_samples

	###### Analyze with punkProse
	echo "Dont forget to change the parameters.yaml of punkProse!"
	cd ${PUNKPROSE}
	mkdir out_predictions
	python3 punctuator.py -m ${MODELNAME} -d ${PUNKPROSE}/corpus/test_samples/ -o out_predictions/ -p parameters.yaml
	echo "Transcription with punctuation:"
	cat ${PUNKPROSE}/out_predictions/"${INPUT/.wav/.txt}"
	echo "The annotated transcription file is in" ${PUNKPROSE}/out_predictions

fi


if [ ${stage} -le 5 ]; then
	##### Remove any intermediate results we dont need anymore
	echo "Stage 5: Removing all intermediate results"
	# output from espnet
	#rm ${ALIGNER}/"${INPUT/.wav/.txt}"

	# input/output from aligner
	rm ${ALIGNER}/"${INPUT/.wav/.words}"
	rm ${ALIGNER}/"${INPUT/.wav/.mfc}"
	rm ${ALIGNER}/"${INPUT/.wav/.align}"

	# input/output from proscripter
	rm -rf ${PROSCRIPTER}/out_predictions

	# input for punkProse
	rm -rf ${PUNKPROSE}/corpus

fi
