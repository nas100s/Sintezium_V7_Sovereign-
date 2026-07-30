import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';
import { createKernelAccount } from '@zerodev/sdk';
import { signerToEcdsaValidator } from '@zerodev/ecdsa-validator';
import { getEntryPoint, KERNEL_V3_1 } from '@zerodev/sdk/constants';
import { createSmartAccountClient } from 'permissionless';
import { createPimlicoPaymasterClient } from 'permissionless/clients/pimlico';
import * as fs from 'fs';
import * as dotenv from 'dotenv';

dotenv.config({ path: '/opt/sintezium/core/.env' });

const PIMLICO_URL = `https://api.pimlico.io/v2/1/rpc?apikey=${process.env.PIMLICO_API_KEY}`;
const PUBLIC_RPC = process.env.ETH_MAINNET_RPC || 'https://eth.llamarpc.com';
const entryPoint = getEntryPoint('0.7');

const main = async () => {
    console.log('\n[ETH MAINNET] Запуск безгазового деплоя контракта (Zero-Gas)...');
    
    // Чтение байткода из скомпилированного артефакта
    const artifactPath = '/opt/sintezium/ethereum_core/artifacts/contracts/Sintezium_Element_119_Absolute.sol/Sintezium_Element_119.json';
    if (!fs.existsSync(artifactPath)) throw new Error('Артефакт не найден. Скомпилируйте контракт!');
    
    const artifact = JSON.parse(fs.readFileSync(artifactPath, 'utf8'));
    const bytecode = artifact.bytecode;

    const publicClient = createPublicClient({ chain: mainnet, transport: http(PUBLIC_RPC) });
    const pimlicoPaymaster = createPimlicoPaymasterClient({ transport: http(PIMLICO_URL), entryPoint });
    const signer = privateKeyToAccount(process.env.PAYMASTER_KEY as `0x${string}`);
    
    const ecdsaValidator = await signerToEcdsaValidator(publicClient, {
        signer, entryPoint, kernelVersion: KERNEL_V3_1
    });

    const account = await createKernelAccount(publicClient, {
        plugins: { sudo: ecdsaValidator },
        entryPoint, kernelVersion: KERNEL_V3_1
    });

    console.log('[SUCCESS] Smart Account (Kernel):', account.address);

    const smartAccountClient = createSmartAccountClient({
        account,
        entryPoint,
        chain: mainnet,
        bundlerTransport: http(PIMLICO_URL),
        middleware: {
            sponsorUserOperation: pimlicoPaymaster.sponsorUserOperation,
        }
    });

    console.log('\n[EXECUTION] Отправка UserOperation для создания смарт-контракта...');

    const txHash = await smartAccountClient.sendTransaction({
        to: undefined as any, 
        value: BigInt(0),
        data: bytecode as `0x${string}`
    });

    console.log('\n[🚀 ABSOLUTE SUCCESS] Контракт Синтезиум 119 отправлен в Ethereum Mainnet!');
    console.log('🔗 Etherscan: https://etherscan.io/tx/' + txHash);
};

main().catch(console.error);
